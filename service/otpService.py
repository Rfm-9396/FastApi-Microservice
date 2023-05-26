from datetime import datetime, timedelta
from utils.EncryptPin import encrypt_pin, decrypt_pin
from uuid import uuid4
from dtos.dtos import GenerationResponse, OtpValidationResponse, GetPinResponse, OtpHistoryResponse, \
    OtpInvalidationResponse


import certifi as certifi
import motor.motor_asyncio

from schemas import Otp, OtpHistory

from config import Settings
from utils.pinGen import pinGen

configs = Settings()

client = motor.motor_asyncio.AsyncIOMotorClient(configs.MONGO_VAR,tlsCAFile=certifi.where())
db = client.Fast  # database name
otpCollection = db.FastAPICollection  # collection name


async def generate_otp(api_client_id):
    gen_id = str(uuid4())
    api_client_id = api_client_id
    otp_pin = pinGen()
    encrypted_pin = encrypt_pin(otp_pin)

    otp_history = OtpHistory(
        stateId=0,
        stateDescription="OTP Generated",
        stateDate=datetime.now()
    )


    otp = Otp(
        genId=gen_id,
        otpPin=encrypted_pin,
        currentStatus=0,
        apiClientId=api_client_id,
        stateHistory=[otp_history],
        expiryOn=datetime.now() + timedelta(minutes=configs.TTL)
    )

    generation_response = GenerationResponse(
        message="OTP Generated",
        genId=gen_id,
        otpPin=otp_pin,
        apiClientId=api_client_id,
        currentStatus=0,
        expiryOn=otp.expiryOn
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
    print(decrypt_pin(otp['otpPin']))
    print(otp_validation_request.otpPin)
    # All validations passed ___________________________________________________________________________________________
    if int(decrypt_pin(otp['otpPin'])) == otp_validation_request.otpPin:
        print('im here')
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
        print('im here 2')
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
            message="OTP Found",
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
    if int(decrypt_pin(otp['otpPin'])) != otp_invalidation_request.otpPin:
        return OtpInvalidationResponse(
            message="Invalid OTP PIN"
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
