import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

# retriving the mongo url from .env
MONGO_DETAILS = config("MONGO_URL")


def connection(collection: str):
    MONGO_DETAILS = "mongodb+srv://vaibhav:Vaibhav%40143@cluster0.nm9w35r.mongodb.net/?retryWrites=true&w=majority"
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    database = client.chainner
    return database.get_collection(collection)

