from app.server.security.auth import (check_api_data)
from app.server.models.apikey import (
    ErrorResponseModel,
    ResponseModel,
)
from app.server.models.nlpservices import (
    KeyphrasesSchema, TopicmodellingSchema, SentimentanalysisSchema)
from app.server.database import (
    add_log
)
from app.server.security.auth_bearer import JWTBearer
from fastapi import APIRouter, Header, HTTPException, Request, Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from decouple import config
import httpx

nlp_api_endpoint = config("NLP_MODEL_API_ENDPOINT")

router = APIRouter()


@router.get("/", dependencies=[Depends(JWTBearer())], response_description="Health check NLP models")
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
                        "apikey": request.headers.get("apikey"),
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
                        "apikey": request.headers.get("apikey"),
                        "timestamp": datetime.now().isoformat(),
                        "method": request.method,
                        "url": request.url,
                        "headers": str(request.headers) if request.headers else "None",
                        "client": str(request.client.host) if request.client.host else "None",
                        "response": str('Request to NLP 3rd-party API failed')
                    }
                    log_request_body = jsonable_encoder(log_request)
                    await add_log(log_request_body)
                    raise HTTPException(
                        status_code=response.status_code, detail="Request to NLP 3rd-party API failed")
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


@router.post("/keyphrases", dependencies=[Depends(JWTBearer())], response_description="content tagging")
async def keyphrases_process(request: Request, payload: KeyphrasesSchema, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        req_info = await request.json()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{nlp_api_endpoint}/api/v1/keyphrases/", json=req_info["comments"], timeout=None)
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


@router.post("/topic-modeling", dependencies=[Depends(JWTBearer())], response_description="Topic modeling")
async def topic_modeling_process(request: Request, payload: TopicmodellingSchema, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        req_info = await request.json()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{nlp_api_endpoint}/api/v1/topic-modeling/", json=req_info, timeout=None)
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


@router.post("/sentiment-analysis", dependencies=[Depends(JWTBearer())], response_description="sentiment-analysis")
async def sentiment_analysis_modeling_process(request: Request, payload: SentimentanalysisSchema, apikey: str = Header(None)):
    if not apikey:
        return ErrorResponseModel('error', 400, 'API Key is missing in the header')
    is_valid_apikey = await check_api_data(apikey)

    if not is_valid_apikey:
        return ErrorResponseModel('error', 403, "Invalid API key")
    else:
        req_info = await request.json()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{nlp_api_endpoint}/api/v1/sentiment-analysis/", json=req_info, timeout=None)
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
