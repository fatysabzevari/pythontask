from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models import TeamSchema

from database import *
from models import (
    UserSchema,ResponseModel, ErrorResponseModel

)
from fastapi import HTTPException

router = APIRouter()


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    try:
        user = jsonable_encoder(user)
        new_user = await add_user(user)
        return ResponseModel(new_user, "user added successfully.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")



@router.get("/", response_description="users retrieved")
async def get_all_users():
    users = await get_users()
    if users:
        return ResponseModel(users, "users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "user doesn't exist.")

@router.post("/teams/", response_description="Team added into the database")
async def add_team_data(team: TeamSchema = Body(...)):
    try:
        team = jsonable_encoder(team)
        new_team = await add_team(team)
        return ResponseModel(new_team, "Team added successfully.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/teams/", response_description="Teams retrieved")
async def get_all_teams():
    teams = await get_teams()
    if teams:
        return ResponseModel(teams, "Teams data retrieved successfully")
    return ResponseModel(teams, "Empty list returned")
