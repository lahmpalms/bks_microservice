from fastapi import APIRouter, Body, Header, Security, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import APIKeyHeader

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

from server.security.auth import (check_api_data)

router = APIRouter()


@router.post("/", response_description="apikey generate data added into the database")
async def add_api_data(apikey: ApikeySchema = Body(...)):
    apikey = jsonable_encoder(apikey)
    new_api = await add_apikey(apikey)
    return ResponseModel(new_api, "apikey generate added successfully.")


@router.get("/", response_description="apikey get data from the database")
async def get_api_data(apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)
    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            all_apikey = await retrieve_apikeys()
            if all_apikey:
                return ResponseModel(all_apikey, "apikey data retrieved successfully")
            return ResponseModel(all_apikey, "Empty list returned")
        except Exception:
            return ErrorResponseModel('error', 500, 'Internal Server Error')
