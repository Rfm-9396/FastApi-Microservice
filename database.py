from datetime import datetime
from random import random
from uuid import uuid4

from schemas import Otp, OtpHistory

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://admin:ctt123@cluster0.voemkxz.mongodb.net')
db = client.FastApiOtp # database name
OtpCollection = db.get_collection("OtpCollection") # collection name


