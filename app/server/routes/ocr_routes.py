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


load_dotenv()
ocr_api_endpoint = os.getenv('OCR_MODEL_API_ENDPOINT')

router = APIRouter()


@router.get("/", dependencies=[Depends(JWTBearer())], response_description="health check ocr models")
async def health_check(request: Request, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ocr_api_endpoint}")
                if response.status_code == 200:
                    log_request = {
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to OCR 3rd-party API successful')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    return ResponseModel(None, "Request to OCR 3rd-party API successful")
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
                        status_code=response.status_code, detail="Request to OCR 3rd-party API failed")
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


@router.post("/ocr_files", dependencies=[Depends(JWTBearer())], response_description="processing files on ocr models")
async def process_on_ocr_models(response: Response, request: Request, apikey: str = Header(None), files: List[UploadFile] = File(...)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')

    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")

    try:
        async with httpx.AsyncClient() as client:
            form_data = [("files", (file.filename, file.file))
                         for file in files]
            response = await client.post(f"{ocr_api_endpoint}/ocr_file", files=form_data)
            print(response.json())
            if response.status_code == 201:
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
                return ResponseModel(response.json(), 'Request to OCR 3rd-party API successful')
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
                return ErrorResponseModel('error', response.status_code, 'Request to OCR 3rd-party API failed')
    except Exception:
        log_request = {
            "timestamp": datetime.now().isoformat(),
            "method": request.method,
            "url": request.url,
            "headers": str(request.headers) if request.headers else "None",
            "client": str(request.client.host) if request.client.host else "None",
            "response": 'Internal Server Error'
        }
        log_request_body = jsonable_encoder(log_request)
        await add_log(log_request_body)
        return ErrorResponseModel('error', 500, 'Internal Server Error')
