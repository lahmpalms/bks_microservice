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


@router.post("/", response_description="apikey generate data added into the database")
async def add_api_data(apikey: ApikeySchema = Body(...)):
    apikey = jsonable_encoder(apikey)
    new_api = await add_apikey(apikey)
    return ResponseModel(new_api, "apikey generate added successfully.")


@router.get("/", response_description="apikey get data from the database")
async def get_api_data():
    try:
        all_apikey = await retrieve_apikeys()
        if all_apikey:
            return ResponseModel(all_apikey, "apikey data retrieved successfully")
        return ResponseModel(all_apikey, "Empty list returned")
    except Exception:
        return ErrorResponseModel('error', 500, 'Internal Server Error')
