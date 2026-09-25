from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DB

client = None
database = None

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=2000
    )

    client.admin.command("ping")

    database = client[MONGO_DB]

except Exception:
    client = None
    database = None


def get_database():

    return database