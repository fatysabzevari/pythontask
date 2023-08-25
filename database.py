import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.company

user_collection = database.get_collection("users_collection")
team_collection = database.get_collection("teams_collection")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["fullname"],
        "gender": user["gender"],
        "age": user["age"],
    }



# get all users present in the database
async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


def team_helper(team, users) -> dict:
    members = team["members"]
    sorted_members = sorted(
        (user for user in users if user["id"] in members),
        key=lambda member: member["age"]
    )
    return {
        "id": str(team["_id"]),
        "title": team["title"],
        "members": sorted_members,
    }


async def get_teams():
    users = await get_users()
    teams = []
    async for team in team_collection.find():
        teams.append(team_helper(team, users))
    return teams


async def add_team(team_data: dict) -> dict:
    team = await team_collection.insert_one(team_data)
    new_team = await team_collection.find_one({"_id": team.inserted_id})
    return team_helper(new_team)