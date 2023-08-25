# import motor.motor_asyncio
# from bson.objectid import ObjectId
#
#
# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
# class MongoConnection:
#     client = None
#
#     def __init__(self):
#         self.client = motor.motor_asyncio.AsyncIOMotorClient(
#             "mongodb://localhost:27017",
#             username="your_username",
#             password="your_password"
#         ) if not self.client else self.client
#
#         self.db = self.client["company"]
#         self.user1 = self.db["user1"]  # تغییر نام کالکشن به "user1"
#         self.teams= self.db["teams"]  # تغییر نام کالکشن به "teams"
#
#     def __enter__(self):
#         return self
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         await self.client.close()
#
# def user_helper(user) -> dict:
#     return {
#         "id": str(user["_id"]),
#         "name": user["name"],
#         "gender": user["gender"],
#         "age": user["age"],
#     }
#
#
#
# # get all users present in the database
# async def get_users():
#     users = []
#     async for user in user1.find():
#         users.append(user_helper(user))
#     return users
#
#
# # Add a new user into to the database
# async def add_user(user_data: dict) -> dict:
#     user = await user_collection.insert_one(user_data)
#     new_user = await user_collection.find_one({"_id": user.inserted_id})
#     return user_helper(new_user)
#
#
# # Retrieve a user with a matching ID
# async def retrieve_user(id: str) -> dict:
#     user = await user_collection.find_one({"_id": ObjectId(id)})
#     if user:
#         return user_helper(user)
#
#
# # Update a user with a matching ID
# async def update_user(id: str, data: dict):
#     # Return false if an empty request body is sent.
#     if len(data) < 1:
#         return False
#     user = await user_collection.find_one({"_id": ObjectId(id)})
#     if user:
#         updated_user = await user_collection.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_user:
#             return True
#         return False
#
#
# # Delete a user from the database
# async def delete_user(id: str):
#     user = await user_collection.find_one({"_id": ObjectId(id)})
#     if user:
#         await user_collection.delete_one({"_id": ObjectId(id)})
#         return True
#
#
# def team_helper(team, users) -> dict:
#     members = team["members"]
#     sorted_members = sorted(
#         (user for user in users if user["id"] in members),
#         key=lambda member: member["age"]
#     )
#     return {
#         "id": str(team["_id"]),
#         "title": team["title"],
#         "members": sorted_members,
#     }
#
#
# async def get_teams():
#     users = await get_users()
#     teams = []
#     async for team in team_collection.find():
#         teams.append(team_helper(team, users))
#     return teams
#
#
# async def add_team(team_data: dict) -> dict:
#     team = await team_collection.insert_one(team_data)
#     new_team = await team_collection.find_one({"_id": team.inserted_id})
#     return team_helper(new_team)


import motor.motor_asyncio
from bson.objectid import ObjectId

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MongoConnection:
    client = None

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://localhost:27017",
            username="your_username",
            password="your_password"
        ) if not self.client else self.client

        self.db = self.client["company"]
        self.user1 = self.db["user1"]  # تغییر نام کالکشن به "user1"
        self.teams = self.db["teams"]  # تغییر نام کالکشن به "teams"

    def __enter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()

def user_helper(user) -> dict:
    """
    Helper function to create a dictionary from user data.

    Args:
        user (dict): User data retrieved from the database.

    Returns:
        dict: Dictionary containing user data.
    """

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "gender": user["gender"],
        "age": user["age"],
    }


async def get_users():
    """
    Retrieve a list of all users from the database.

    Returns:
        list: List of dictionaries containing user data.
    """
    users = []
    async for user in MongoConnection().user1.find():
        users.append(user_helper(user))
    return users

async def add_user(user_data: dict) -> dict:
    """
       Add a new user to the database.
   """
    user = await MongoConnection().user1.insert_one(user_data)
    new_user = await MongoConnection().user1.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(id: str) -> dict:
    """
    Retrieve a user with a matching ID from the database.
    """
    user = await MongoConnection().user1.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def update_user(id: str, data: dict):
    """
    Update a user with a matching ID in the database.
    """
    if len(data) < 1:
        return False
    user = await MongoConnection().user1.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await MongoConnection().user1.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(id: str):
    """
    Delete a user with a matching ID from the database.
    """
    user = await MongoConnection().user1.find_one({"_id": ObjectId(id)})
    if user:
        await MongoConnection().user1.delete_one({"_id": ObjectId(id)})
        return True


def team_helper(team, users) -> dict:
    """
    Helper function to create a dictionary from team data.
    """
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
    """
    Retrieve a list of all teams from the database.
    """
    users = await get_users()
    teams = []
    async for team in MongoConnection().teams.find():
        teams.append(team_helper(team, users))
    return teams


async def add_team(team_data: dict) -> dict:
    """
    Add a new team to the database.

    Args:
        team_data (dict): Data for the new team.

    Returns:
        dict: Dictionary containing data of the added team.
    """
    team = await MongoConnection().teams.insert_one(team_data)
    new_team = await MongoConnection().teams.find_one({"_id": team.inserted_id})
    return team_helper(new_team)
