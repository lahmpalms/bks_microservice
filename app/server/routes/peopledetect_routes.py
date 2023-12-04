from server.security.auth import (check_api_data)
from server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
)
from server.database import (
    add_log
)
from server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Header, HTTPException, Request, Depends, Response, File, UploadFile
from fastapi.encoders import jsonable_encoder
import httpx
from datetime import datetime
from decouple import config
from typing import List

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
                response = await client.get(f"{peopledetect_api_endpoint}/getlogclouddata")
                print('response', response.json())
                if response.status_code == 200:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
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
                        "apikey": request.headers.get("apikey"),
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
                "apikey": request.headers.get("apikey"),
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


@router.post("/detect-people", dependencies=[Depends(JWTBearer())], response_description="processing files people detect models")
async def peopledetect_process(response: Response, request: Request, apikey: str = Header(None), files: List[UploadFile] = File(...)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        form_data = [("image", file.file)
                     for file in files]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{peopledetect_api_endpoint}/detect-people/", files=form_data, timeout=None)
                print('response', response)
                if response.status_code == 200:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
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
                        "apikey": request.headers.get("apikey"),
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
                "apikey": request.headers.get("apikey"),
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


@router.post("/detect_faces", dependencies=[Depends(JWTBearer())], response_description="processing files to detect faces on people detect models")
async def facedetect_process(response: Response, request: Request, apikey: str = Header(None), files: List[UploadFile] = File(...)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        form_data = [("image", file.file)
                     for file in files]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{peopledetect_api_endpoint}/detect_faces/", files=form_data, timeout=None)
                print('response', response)
                if response.status_code == 200:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
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
                        "apikey": request.headers.get("apikey"),
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
                "apikey": request.headers.get("apikey"),
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


@router.post("/gender-classification", dependencies=[Depends(JWTBearer())], response_description="processing files to detect faces on people detect models")
async def gender_classification_process(response: Response, request: Request, apikey: str = Header(None), files: List[UploadFile] = File(...)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        form_data = [("image", file.file)
                     for file in files]
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{peopledetect_api_endpoint}/gender-classifications", files=form_data, timeout=None)
                print('response', response)
                if response.status_code == 200:
                    log_request = {
                        "apikey": request.headers.get("apikey"),
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
                        "apikey": request.headers.get("apikey"),
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
                "apikey": request.headers.get("apikey"),
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