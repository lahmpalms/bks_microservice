from fastapi import FastAPI,  HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from server.routes.apikey import router as ApikeyRouter
import time
import os
from dotenv import load_dotenv

load_dotenv()
api_endpoint = os.getenv('API_ENDPOINT')


app = FastAPI()


app.include_router(ApikeyRouter, tags=[
                   "Apikey"], prefix=f"{api_endpoint}/apikey")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
