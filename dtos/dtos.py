from datetime import datetime

from pydantic import BaseModel


class GenerationRequest(BaseModel):
    apiClientId: str


class GenerationResponse(BaseModel):
    message: str
    genId: str
    otpPin: int
    apiClientId: str
    expiryOn: datetime
    currentStatus: int


class GetPinRequest(BaseModel):
    genId: str


class GetPinResponse(BaseModel):
    genId: str
    otpPin: int
    currentStatus: int
    apiClientId: str
    expiryOn: datetime
    stateHistory: list


class OtpValidationRequest(BaseModel):
    genId: str
    otpPin: int
    apiClientId: str
    receiverName: str


class OtpValidationResponse(BaseModel):
    message: str


class OtpHistoryRequest(BaseModel):
    genId: str
    apiClientId: str


class OtpHistoryResponse(BaseModel):
    message: str
    stateHistory: list | None


class OtpInvalidationRequest(BaseModel):
    genId: str
    apiClientId: str
    otpPin: int


class OtpInvalidationResponse(BaseModel):
    message: str
