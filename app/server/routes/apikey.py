from app.server.security.auth import (check_api_data, signJWT, signupJWT)
from app.server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
    ApikeySchema,
    UserLoginSchema
)
from app.server.database import (
    retrieve_apikeys,
    add_apikey,
    add_log,
    check_userdata
)
from app.server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Body, Header, Request, Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime


router = APIRouter()


async def check_user(data: UserLoginSchema):
    is_valid_apikey = await check_userdata(data)
    return is_valid_apikey


@router.post("/user/login", tags=["OAuth"])
async def user_login(user: UserLoginSchema = Body(...)):
    user_login = await check_user(user)
    if user_login:
        return signJWT(user_login)
    else:
        return {
            "error": "Wrong login details!"
        }


@router.post("/user/signup", dependencies=[Depends(JWTBearer())], tags=["OAuth"])
async def create_user(user: ApikeySchema = Body(...)):
    apikey = jsonable_encoder(user)
    new_api = await add_apikey(apikey)
    return signupJWT(user)


@router.post("/", dependencies=[Depends(JWTBearer())], response_description="apikey generate data added into the database")
async def add_api_data(apikey: ApikeySchema = Body(...)):
    apikey = jsonable_encoder(apikey)
    new_api = await add_apikey(apikey)
    return ResponseModel(new_api, "apikey generate added successfully.")


@router.get("/", dependencies=[Depends(JWTBearer())], response_description="apikey get data from the database")
async def get_api_data(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            all_apikey = await retrieve_apikeys()
            if all_apikey:
                log_request = {
                    "apikey": request.headers.get("apikey"),
                    "timestamp": datetime.now().isoformat(),
                    "method": request.method,
                    "url": request.url,
                    "headers": str(request.headers) if request.headers else "None",
                    "client": str(request.client.host) if request.client.host else "None",
                    "response": str(all_apikey) if all_apikey else "None"
                }
                log_request_body = jsonable_encoder(log_request)
                await add_log(log_request_body)
                return ResponseModel(all_apikey, "apikey data retrieved successfully")
            return ResponseModel(all_apikey, "Empty list returned")

        except Exception:
            log_request = {
                "apikey": request.headers.get("apikey"),
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "headers": str(request.headers) if request.headers else "None",
                "client": str(request.client.host) if request.client.host else "None",
                "response": str(all_apikey) if all_apikey else "Internal Server Error"
            }
            log_request_body = jsonable_encoder(log_request)
            await add_log(log_request_body)
            return ErrorResponseModel('error', 500, 'Internal Server Error')
