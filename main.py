from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "mydatabase"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
teams_collection = db["teams"]
users_collection = db["users"]

@app.post("/create_user")
async def create_user(name: str, gender: str, age: int):
    user_data = {
        "name": name,
        "gender": gender,
        "age": age
    }
    result = await users_collection.insert_one(user_data)
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

@app.get("/get_users")
async def get_users():
    users = []
    async for user in users_collection.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "gender": user["gender"],
            "age": user["age"]
        })
    return users

@app.get("/teams")
async def get_teams():
    teams_with_members = []

    async for team in teams_collection.find():
        team_data = {
            "title": team["title"],
            "members": []
        }

        for member_id in team["members"]:
            member = await users_collection.find_one({"_id": member_id})
            if member:
                team_data["members"].append({
                    "name": member["name"],
                    "age": member["age"]
                })

        team_data["members"] = sorted(team_data["members"], key=lambda x: x["age"])
        teams_with_members.append(team_data)

    return teams_with_members
