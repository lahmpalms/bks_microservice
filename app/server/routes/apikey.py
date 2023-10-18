from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_apikeys,
    add_apikey
)
from server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
    ApikeySchema,
    UpdateApikeyModel,
)

router = APIRouter()


@router.post("/", response_description="Student data added into the database")
async def add_api_data(apikey: ApikeySchema = Body(...)):
    apikey = jsonable_encoder(apikey)
    new_api = await add_apikey(apikey)
    return ResponseModel(new_api, "Student added successfully.")
