from fastapi import FastAPI,  HTTPException, Security
from fastapi.security import APIKeyHeader
from server.routes.apikey import router as ApikeyRouter
from server.security import auth as Autholization

app = FastAPI()


app.include_router(ApikeyRouter, tags=["Apikey"], prefix="/api/v1/apikey")


@app.get("/", tags=["Root"])
async def read_root():
    resp = await Autholization.get_api_data()
    return {"message": "Welcome to this fantastic app!", 'response': resp}
