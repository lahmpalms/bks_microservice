from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_apikeys,
    find_api
)
from app.server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
    ApikeySchema,
    UpdateApikeyModel,
)


async def check_api_data(user_apikey):
    result = await find_api(user_apikey)
    if result:
        return True  # API key is valid
    else:
        return False  # API key is not found in the database
