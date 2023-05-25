import asyncio
from datetime import datetime
import time
import json
from pymongo import MongoClient

import certifi as certifi
import motor.motor_asyncio
import os

from bson import ObjectId
from typing import Any

from schemas import Otp, OtpHistory

from config import Settings

aa = Settings()


# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
# client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://admin:ctt123@cluster0.voemkxz.mongodb.net',
# tlsCAFile=certifi.where())
client = MongoClient(aa.MONGO_VAR,
                     tlsCAFile=certifi.where())

db = client.Fast  # database name
otpCollection = db.FastAPICollection  # collection name


def status_check():
    otps = otpCollection.find({"currentStatus": 0})
    otps_as_list = list(otps)
    print(f"Total {len(otps_as_list)}")
    skipped = 0
    updated = 0

    for otp in otps_as_list:
        otpModel = Otp(**otp)
        print(otp['expiryOn'])
        if otp['expiryOn'] < datetime.now():
            otp_History = OtpHistory(
                stateId=2,
                stateDescription="OTP Expired",
                stateDate=datetime.now()
            )
            otpModel.stateHistory.append(otp_History)
            otpModel.currentStatus = 2
            otpCollection.update_one({"genId": otp['genId']}, {"$set": otpModel.dict()})

            updated += 1
            print(f"Updated {otp['genId']}")
        else:
            print(f"Skipped {otp['genId']}")
            skipped += 1

    print(f"Updated {updated} and Skipped {skipped}")


status_check()


