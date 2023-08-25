from typing import List
from pydantic import BaseModel, Field
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"


class UserSchema(BaseModel):
    name: str = Field(...)
    gender: Gender
    age: int = Field(...)

    class Config:
        # Example data for documentation purposes
        schema_extra = {
            "example": {
                "name": "sara",
                "gender": "female",
                "age": 25,
            }
        }


class TeamSchema(BaseModel):
    """
    Schema to define team data.
    """
    title: str = Field(...)
    members: List[str] = Field(...)

    class Config:
        """
        Extra configuration for TeamSchema.
        """
        schema_extra = {
            "example": {
                "title": "Development Team",
                "members": ["user_id_1", "user_id_2"],
            }
        }


def ResponseModel(data, message):
    """
    Create a response model for successful requests.

    Args:
        data: The data to be included in the response.
        message: The message to be included in the response.

    Returns:
        dict: A dictionary containing the response model.
    """
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    """
    Create a response model for error responses.

    Args:
        error: The error message.
        code: The error code.
        message: The message to be included in the response.

    Returns:
        dict: A dictionary containing the error response model.
    """
    return {"error": error, "code": code, "message": message}
