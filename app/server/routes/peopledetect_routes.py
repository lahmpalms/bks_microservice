from server.security.auth import (check_api_data)
from server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
)
from server.database import (
    add_log
)

from fastapi import APIRouter, Body, Header, Security, HTTPException, Response, Request, File, Form, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.security import APIKeyHeader

import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List
import shutil

from server.security.auth_bearer import JWTBearer

from decouple import config

peopledetect_api_endpoint = config("PEOPLE_DETECT_MODEL_API_ENDPOINT")

router = APIRouter()


@router.get("/all-logs", dependencies=[Depends(JWTBearer())], response_description="Get all logs from people detect models")
async def get_all_logs(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{peopledetect_api_endpoint}/alllogs")
                print('response', response.json())
                if response.status_code == 200:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": response.json()
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    return ResponseModel(response.json(), "Request to PEOPLE-DETECT 3rd-party API successful")
                else:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to PEOPLE-DETECT 3rd-party API failed')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    raise HTTPException(
                        status_code=response.status_code, detail="Request to PEOPLE-DETECT 3rd-party API failed")
        except Exception:
            log_request = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "headers": str(request.headers) if request.headers else "None",
                "client": str(request.client.host) if request.client.host else "None",
                "response": str('Internal Server Error')
            }
            log_request_body = jsonable_encoder(log_request)
            await add_log(log_request_body)
            return ErrorResponseModel('error', 500, 'Internal Server Error')


@router.get("/logs/{logs_id}", dependencies=[Depends(JWTBearer())], response_description="Get logs detail from people detect models")
async def get_logs_detail(logs_id: str, request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            async with httpx.AsyncClient() as client:
                print('logs_id', logs_id)
                response = await client.get(f"{peopledetect_api_endpoint}/logs/{logs_id}")
                print('response', response.json())
                if response.status_code == 200:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": response.json()
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    return ResponseModel(response.json(), "Request to PEOPLE-DETECT 3rd-party API successful")
                else:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to PEOPLE-DETECT 3rd-party API failed')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    raise HTTPException(
                        status_code=response.status_code, detail="Request to PEOPLE-DETECT 3rd-party API failed")
        except Exception:
            log_request = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "headers": str(request.headers) if request.headers else "None",
                "client": str(request.client.host) if request.client.host else "None",
                "response": str('Internal Server Error')
            }
            log_request_body = jsonable_encoder(log_request)
            await add_log(log_request_body)
            return ErrorResponseModel('error', 500, 'Internal Server Error')
