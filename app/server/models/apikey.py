from typing import Optional
import secrets
from pydantic import BaseModel, EmailStr, Field


def GenerateApiKey():
    generated_key = secrets.token_urlsafe(32)
    return generated_key


class ApikeySchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    apikey: str = GenerateApiKey()

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
            }
        }


class UpdateApikeyModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    apikey: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe Test",
                "email": "jdoe@x.edu.ng",
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
