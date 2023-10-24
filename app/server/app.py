from fastapi import FastAPI,  HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from server.routes.apikey import router as ApikeyRouter
from server.routes.ocr_routes import router as OcrRouter
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint = os.getenv('API_ENDPOINT')


app = FastAPI()


app.include_router(ApikeyRouter, tags=[
                   "apikey_sevice"], prefix=f"{api_endpoint}/apikey")

app.include_router(OcrRouter, tags=["ocr_service"], prefix=f"{api_endpoint}/ocr")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
