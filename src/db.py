"""Handles the MongoDB connection for the project."""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

USERNAME = os.getenv("MONGO_ROOT_USERNAME")
PASSWORD = os.getenv("MONGO_ROOT_PASSWORD")
AUTH_DB = os.getenv("AUTH_DATABASE_NAME")
DB_NAME = os.getenv("MONGO_DB_NAME")

CONNECTION_STR = (
    f"mongodb://{USERNAME}:{PASSWORD}"
    f"@localhost:27017/{DB_NAME}"
    f"?authSource={AUTH_DB}"
)

def get_db():
    """Return a (client, db) pair. Caller is responsible for closing the client."""
    client = MongoClient(CONNECTION_STR)
    return client, client[DB_NAME]
