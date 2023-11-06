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

nlp_api_endpoint = config("NLP_MODEL_API_ENDPOINT")

router = APIRouter()


@router.get("/", response_description="health check NLP models")
async def health_check(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{nlp_api_endpoint}/api/v1/")
                print('response', response)
                if response.status_code == 200:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to NLP 3rd-party API successful')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    return ResponseModel(None, "Request to NLP 3rd-party API successful")
                else:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to OCR 3rd-party API failed')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    raise HTTPException(
                        status_code=response.status_code, detail="Request to NLP 3rd-party API failed")
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


@router.post("/keyphrases", response_description="content tagging")
async def keyphrases_process(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        req_info = await request.json()
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(f"{nlp_api_endpoint}/api/v1/keyphrases/", json=req_info, timeout=None)
        #     print('res', response.json())
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{nlp_api_endpoint}/api/v1/keyphrases/", json=req_info, timeout=None)
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
                    return ResponseModel(response.json(), "Request to NLP 3rd-party API successful")
                else:
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
                    return ErrorResponseModel('error', response.status_code, 'Request to NLP 3rd-party API failed')
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
