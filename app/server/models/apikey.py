from typing import Optional
import secrets
from pydantic import BaseModel, EmailStr, Field


def GenerateApiKey():
    generated_key = secrets.token_urlsafe(32)
    return generated_key


class ApikeySchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    apikey: str = GenerateApiKey()

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Test example",
                "email": "test@x.edu.ng",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
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
