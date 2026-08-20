"""Writes transformed documents into MongoDB using bulk_write."""

from pymongo import ReplaceOne
from pymongo.errors import BulkWriteError


class Loader:
    """Loads product and review documents into their collections."""

    def __init__(self, db):
        self.db = db

    def load_products(self, documents):
        """Upsert product documents into the products collection, keyed on asin."""
        return self._load(self.db["products"], documents, key="asin")

    def load_reviews(self, documents):
        """Upsert review documents into the reviews collection, keyed on reviewID."""
        return self._load(self.db["reviews"], documents, key="reviewID")

    def _load(self, collection, documents, key):
        """Build a ReplaceOne upsert per document and run it as one bulk_write call."""
        if not documents:
            return 0

        operations = [
            ReplaceOne({key: doc[key]}, doc, upsert=True) for doc in documents
        ]

        try:
            result = collection.bulk_write(operations, ordered=False)
            return result.upserted_count + result.modified_count
        except BulkWriteError as e:
            print(f"Some writes failed loading into {collection.name}: {e.details}")
            return e.details.get("nUpserted", 0) + e.details.get("nModified", 0)
