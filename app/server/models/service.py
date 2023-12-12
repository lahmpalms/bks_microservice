from typing import Optional, List
import secrets
from pydantic import BaseModel, EmailStr, Field


class ServiceSchema(BaseModel):
    service_name: str
    apikey: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "service_name": "service_name",
                "apikey": ["test"],
            }
        }
