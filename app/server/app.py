from fastapi import FastAPI
from server.routes.apikey import router as ApikeyRouter

app = FastAPI()

app.include_router(ApikeyRouter, tags=["Apikey"], prefix="/api/v1/apikey")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
