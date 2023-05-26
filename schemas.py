from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId


class OtpHistory(BaseModel):
    stateId: int
    stateDescription: str
    stateDate: datetime


class Otp(BaseModel):
    genId: str
    otpPin: str
    apiClientId: str
    expiryOn: datetime
    currentStatus: int # 0 - Active, 1 - Inactive
    stateHistory: List[OtpHistory]

