"""Creates MongoDB collections, validators, and indexes. Safe to re-run."""

import os

from dotenv import load_dotenv
from pymongo import ASCENDING, MongoClient
from pymongo.errors import CollectionInvalid

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

PRODUCTS_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["asin", "title"],
        "properties": {
            "asin": {"bsonType": "string"},
            "title": {"bsonType": "string"},
        },
    }
}

REVIEWS_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["reviewID", "productASIN"],
        "properties": {
            "reviewID": {"bsonType": "string"},
            "productASIN": {"bsonType": "string"},
        },
    }
}


def create_collection_if_missing(db, name, validator):
    """Create a collection with a validator, or do nothing if it already exists."""
    if name in db.list_collection_names():
        return
    try:
        db.create_collection(name, validator=validator)
    except CollectionInvalid:
        pass


def create_index_if_missing(collection, keys, **kwargs):
    """Create an index, or do nothing if one with the same name already exists."""
    index_name = kwargs.get("name")
    existing_names = [idx["name"] for idx in collection.list_indexes()]
    if index_name in existing_names:
        return
    collection.create_index(keys, **kwargs)


def setup_products_indexes(db):
    products = db["products"]
    create_index_if_missing(products, [("asin", ASCENDING)], unique=True, name="asin_unique")


def setup_reviews_indexes(db):
    reviews = db["reviews"]
    create_index_if_missing(reviews, [("reviewID", ASCENDING)], unique=True, name="reviewID_unique")
    create_index_if_missing(reviews, [("productASIN", ASCENDING)], name="productASIN_idx")
    create_index_if_missing(reviews, [("rating", ASCENDING)], name="rating_idx")
    create_index_if_missing(
        reviews,
        [("productASIN", ASCENDING), ("rating", ASCENDING)],
        name="productASIN_rating_compound",
    )


def main():
    client = MongoClient(CONNECTION_STR)
    db = client[DB_NAME]

    create_collection_if_missing(db, "products", PRODUCTS_VALIDATOR)
    create_collection_if_missing(db, "reviews", REVIEWS_VALIDATOR)

    setup_products_indexes(db)
    setup_reviews_indexes(db)

    client.close()


if __name__ == "__main__":
    main()