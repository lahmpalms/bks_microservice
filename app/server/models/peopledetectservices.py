from typing import List
from pydantic import BaseModel, Field, EmailStr, AnyHttpUrl
from fastapi import File, UploadFile


class FormDataSchema(BaseModel):
    images: List[UploadFile] = File(..., description="List of image files")

    class Config:
        schema_extra = {
            "example": {
                "images": ["image1.jpg", "image2.png"],
            }
        }
