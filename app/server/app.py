from fastapi import FastAPI,  HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from app.server.routes.apikey import router as ApikeyRouter
from app.server.routes.ocr_routes import router as OcrRouter
from app.server.routes.nlp_routes import router as NLPRouter
from app.server.routes.peopledetect_routes import router as PeopledetectRouter
import time
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
api_endpoint = os.getenv('API_ENDPOINT')


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ApikeyRouter, tags=[
                   "apikey_sevice"], prefix=f"{api_endpoint}/apikey")

app.include_router(
    OcrRouter, tags=["ocr_service"], prefix=f"{api_endpoint}/ocr")

app.include_router(
    NLPRouter, tags=["nlp_service"], prefix=f"{api_endpoint}/nlp")

app.include_router(
    PeopledetectRouter, tags=["peopledetect_service"], prefix=f"{api_endpoint}/peopledetect")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
