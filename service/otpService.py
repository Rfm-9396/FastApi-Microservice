from datetime import datetime, timedelta
from random import random
from uuid import uuid4
from dtos.dtos import GenerationResponse, OtpValidationResponse, GetPinResponse, OtpHistoryResponse, \
    OtpInvalidationResponse
import os
from dotenv import dotenv_values

import certifi as certifi
import motor.motor_asyncio

from schemas import Otp, OtpHistory

config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

mongo_url = os.environ.get('MONGO_URL')

# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://admin:ctt123@cluster0.voemkxz.mongodb.net',
                                                tlsCAFile=certifi.where())
db = client.Fast  # database name
otpCollection = db.FastAPICollection  # collection name


async def generate_otp(api_client_id):
    gen_id = str(uuid4())
    api_client_id = api_client_id
    otp_pin = int(random() * 10000)

    otp_history = OtpHistory(
        stateId=0,
        stateDescription="OTP Generated",
        stateDate=datetime.now()
    )

    generation_response = GenerationResponse(
        message="OTP Generated",
        genId=str(uuid4()),
        otpPin=int(random() * 10000),
        apiClientId=api_client_id
    )
    otp = Otp(
        genId=gen_id,
        otpPin=otp_pin,
        currentStatus=0,
        apiClientId=api_client_id,
        stateHistory=[otp_history],
        expiryOn=datetime.now() + timedelta(minutes=100)
    )

    result = await otpCollection.insert_one(otp.dict())
    print(datetime.now())
    return generation_response


async def validate_otp(otp_validation_request):
    print(otp_validation_request.genId)

    otp = await otpCollection.find_one({"genId": otp_validation_request.genId})
    # Validations _____________________________________________________________________________________________________
    if otp is None:
        return OtpValidationResponse(
            message="OTP not found"
        )
    if otp['expiryOn'] < datetime.now():
        return OtpValidationResponse(
            message="OTP Expired"
        )
    if otp['currentStatus'] != 0:
        return OtpValidationResponse(
            message="OTP already validated or expired"
        )
    if otp['apiClientId'] != otp_validation_request.apiClientId:
        return OtpValidationResponse(
            message="Invalid API Client Id"
        )
    # All validations passed ___________________________________________________________________________________________
    if otp['otpPin'] == otp_validation_request.otpPin:
        otp_history = OtpHistory(
            stateId=1,
            stateDescription="OTP Validated",
            stateDate=datetime.now()
        )
        otp['currentStatus'] = 1
        otp['stateHistory'].append(otp_history.dict())
        await otpCollection.update_one({"genId": otp['genId']}, {"$set": otp})

        return OtpValidationResponse(
            message="OTP Validated"
        )
    else:
        return OtpValidationResponse(
            message="Invalid OTP PIN"
        )


async def get_pin(gen_id):
    otp = await otpCollection.find_one({"genId": gen_id})
    if otp is None:
        return OtpValidationResponse(
            message="OTP not found"
        )
    else:
        return GetPinResponse(
            genId=otp['genId'],
            otpPin=otp['otpPin'],
            currentStatus=otp['currentStatus'],
            apiClientId=otp['apiClientId'],
            expiryOn=otp['expiryOn'],
            stateHistory=otp['stateHistory']
        )


async def get_otp_history(gen_id, api_client_id):
    otp = await otpCollection.find_one({"genId": gen_id})
    if otp is None:
        return OtpHistoryResponse(
            message="OTP not found"
        )
    if otp['apiClientId'] != api_client_id:
        return OtpHistoryResponse(
            message="Invalid API Client Id"
        )
    else:
        return OtpHistoryResponse(
            message="OTP History",
            stateHistory=otp['stateHistory']
        )


async def invalidate_otp(otp_invalidation_request):
    otp = await otpCollection.find_one({"genId": otp_invalidation_request.genId})
    if otp is None:
        return OtpInvalidationResponse(
            message="OTP not found"
        )
    if otp['apiClientId'] != otp_invalidation_request.apiClientId:
        return OtpInvalidationResponse(
            message="Invalid API Client Id"
        )
    if otp['currentStatus'] != 0:
        return OtpInvalidationResponse(
            message="OTP already validated or expired"
        )
    else:

        otp_history = OtpHistory(
            stateId=2,
            stateDescription="OTP Invalidated",
            stateDate=datetime.now()
        )
        otp['currentStatus'] = 1
        otp['stateHistory'].append(otp_history.dict())
        await otpCollection.update_one({"genId": otp['genId']}, {"$set": otp})

        return OtpInvalidationResponse(
            message="Success: OTP has been Invalidated now"
        )
