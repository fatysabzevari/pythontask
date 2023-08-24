import motor.motor_asyncio

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MongoConnection:
    client = None

    def __init__(self):
        # Check for an existing connection, create one if not present
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://localhost:27017",
            username="your_username",
            password="your_password"
        ) if not self.client else self.client

        # Select the database
        self.db = self.client["company"]
        # Select collections
        self.users_collection = self.db["users"]
        self.teams_collection = self.db["teams"]

    def __enter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Close the connection at the end of operations
        await self.client.close()
