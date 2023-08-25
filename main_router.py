from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models import TeamSchema
from database import *
from models import UserSchema, ResponseModel, ErrorResponseModel
from fastapi import HTTPException

router = APIRouter()

@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    """
    Add user data to the database.

    Args:
        user (UserSchema): User data to be added.

    Returns:
        ResponseModel: Response containing added user data.
    """
    try:
        user = jsonable_encoder(user)
        new_user = await add_user(user)
        return ResponseModel(new_user, "User added successfully.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_description="Users retrieved")
async def get_all_users():
    """
    Retrieve a list of all users from the database.

    Returns:
        ResponseModel: Response containing list of users.
    """
    try:
        users = await get_users()
        if users:
            return ResponseModel(users, "Users data retrieved successfully.")
        return ResponseModel(users, "Empty list returned.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{id}", response_description="User data retrieved")
async def get_user(id):
    """
    Retrieve user data by ID.

    Args:
        id (str): User ID.

    Returns:
        ResponseModel: Response containing retrieved user data.
        ErrorResponseModel: Response indicating error if user is not found.
    """
    try:
        user = await retrieve_user(id)
        if user:
            return ResponseModel(user, "User data retrieved successfully.")
        return ErrorResponseModel("User not found.", 404, "User doesn't exist.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/teams/", response_description="Team added into the database")
async def add_team_data(team: TeamSchema = Body(...)):
    """
    Add a new team to the database.

    Args:
        team (TeamSchema): Team data to be added.

    Returns:
        ResponseModel: Response containing added team data.
    """
    try:
        team = jsonable_encoder(team)
        new_team = await add_team(team)
        return ResponseModel(new_team, "Team added successfully.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/teams/", response_description="Teams retrieved")
async def get_all_teams():
    """
    Retrieve a list of all teams with their members from the database.

    Returns:
        ResponseModel: Response containing list of teams with members.
    """
    try:
        teams = await get_teams()
        if teams:
            return ResponseModel(teams, "Teams data retrieved successfully.")
        return ResponseModel(teams, "Empty list returned.")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal server error")
