from server.models.service import (
    ServiceSchema
)
from server.database import (
    create_service,
    patch_service_apikey,
    check_access_service
)
from server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
)
from server.security.auth import (check_api_data)
from server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Body, Depends, Header
from decouple import config
service_id = config("SERVICE_ADMIN_ID")

router = APIRouter()


@router.post("/service/signup", dependencies=[Depends(JWTBearer())])
async def create_service_apikey_endpoint(service: ServiceSchema = Body(...), apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        is_access = await check_access_service(service_id, apikey)
        if not is_access:
            return ErrorResponseModel('error', 403, "your account is not authorized to access this service")
    apikey = await create_service(service)
    return apikey


@router.patch("/services/{service_id}/update_apikey", dependencies=[Depends(JWTBearer())])
async def patch_service_apikey_endpoint(service_id: str, service: ServiceSchema = Body(...), apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        is_access = await check_access_service(service_id, apikey)
        if not is_access:
            return ErrorResponseModel('error', 403, "your account is not authorized to access this service")
    return await patch_service_apikey(service_id, service)
