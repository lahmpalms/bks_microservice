import time
from typing import Dict

import jwt
from decouple import config

from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_apikeys,
    find_api
)
from server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
    ApikeySchema,
    UpdateApikeyModel,
)

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: dict) -> Dict[str, str]:
    payload = {
        "user_id": user["email"],
        "expires": time.time() + 600,
        "apikey": user["apikey"]
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def signupJWT(user: dict) -> Dict[str, str]:
    payload = {
        "user_id": user.email,
        "expires": time.time() + 600,
        "apikey": user.apikey
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


async def check_api_data(user_apikey):
    result = await find_api(user_apikey)
    if result:
        return True  # API key is valid
    else:
        return False  # API key is not found in the database
