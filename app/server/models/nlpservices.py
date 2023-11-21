from typing import List
from pydantic import BaseModel, Field


class KeyphrasesSchema(BaseModel):
    comments: List[str] = Field(...,
                                description="List of Thai language comments")

    class Config:
        examples = [
            {
                "comments": [
                    "อยากไปทานเลย มีโอกาสต้องไปป",
                    "ถ้าได้ไปแวะแน่นอนครับพี่เบนซ์",
                ]
            }
        ]


class TopicmodellingSchema(BaseModel):
    keyphrases: List[str] = Field(...,
                                  description="List of Thai language comments")
    topics_range: List[int] = Field(
        ..., description="List of integers representing the topics range")

    class Config:
        schema_extra = {
            "example": {
                "keyphrases": [
                    "อยากไปทานเลย มีโอกาสต้องไปป",
                    "ถ้าได้ไปแวะแน่นอนครับพี่เบนซ์",
                    # ... (add more comments)
                ],
                "topics_range": [5]
            }
        }


class SentimentanalysisSchema(BaseModel):
    messages: List[str] = Field(...,
                                description="List of Thai language messages")

    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    "อยากไปทานเลย มีโอกาสต้องไปป อร่อยมากกกกกก"
                    # ... (add more messages if needed)
                ]
            }
        }
