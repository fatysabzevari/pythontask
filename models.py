from typing import List

from pydantic import BaseModel, Field



class UserSchema(BaseModel):
    name: str = Field(...)
    gender: str = Field(...)
    age: int = Field(..., gt=0, lt=100)


    class Config:
        schema_extra = {
            "example": {
                "name": "sara",

                "gender": "female",
                "age": 25,
            }
        }

class TeamSchema(BaseModel):
    title: str = Field(...)
    members: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Development Team",
                "members": ["user_id_1", "user_id_2"],
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