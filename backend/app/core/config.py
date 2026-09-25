import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AI-RecoverX")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB = os.getenv(
    "MONGO_DB",
    "ai_recoverx"
)

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)