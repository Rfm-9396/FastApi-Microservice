from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from statusChecker import status_check
import time


from dtos.dtos import GenerationResponse
from service import otpService

from dtos import dtos

app = FastAPI()
#while True:
#    status_check()
#    time.sleep(60*60)

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/otp/create")
async def root(generation_request: dtos.GenerationRequest):
    generation_response = await otpService.generate_otp(generation_request.apiClientId)
    return generation_response

@app.get("/api/otp/getpin/{genId}")
async def root(genId):
    get_pin_response = await otpService.get_pin(genId)
    return get_pin_response

@app.put("/api/otp/validate")
async def root(otp_validation_request: dtos.OtpValidationRequest):
    otp_validation_response = await otpService.validate_otp(otp_validation_request)
    return otp_validation_response

@app.get("/api/otp/history/{genId}/{apiClientId}")
async def root(genId, apiClientId):
    otp_history_response = await otpService.get_otp_history(genId, apiClientId)
    return otp_history_response

@app.put("/api/otp/invalidate")
async def root(otp_invalidation_request: dtos.OtpInvalidationRequest):
    otp_invalidation_response = await otpService.invalidate_otp(otp_invalidation_request)
    return otp_invalidation_response

