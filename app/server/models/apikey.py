from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ApikeySchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    apikey: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "apikey": "TDnHVp6ed1bFHFS0Bno44Vkly2wSZlNU",  # 32 char alphanum
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
                "apikey": "TDnHVp6ed1bFHFS0Bno44Vkly2wSZlNU",  # 32 char alphanum
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
