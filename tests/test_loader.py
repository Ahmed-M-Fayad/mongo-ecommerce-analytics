"""Tests for the Loader. Checks the bulk write operations it builds, not a live database."""

import sys

sys.path.insert(0, "../src")

from unittest.mock import MagicMock

from pymongo import ReplaceOne

from loader import Loader


def test_load_products_builds_one_replace_one_per_document():
    fake_collection = MagicMock()
    fake_collection.name = "products"
    fake_collection.bulk_write.return_value = MagicMock(upserted_count=2, modified_count=0)

    fake_db = {"products": fake_collection}
    loader = Loader(fake_db)

    docs = [{"asin": "A1", "title": "Product 1"}, {"asin": "A2", "title": "Product 2"}]
    loader.load_products(docs)

    operations = fake_collection.bulk_write.call_args[0][0]
    assert len(operations) == 2
    assert all(isinstance(op, ReplaceOne) for op in operations)


def test_load_products_upserts_are_keyed_on_asin():
    fake_collection = MagicMock()
    fake_collection.name = "products"
    fake_collection.bulk_write.return_value = MagicMock(upserted_count=1, modified_count=0)

    fake_db = {"products": fake_collection}
    loader = Loader(fake_db)

    loader.load_products([{"asin": "A1", "title": "Product 1"}])

    operations = fake_collection.bulk_write.call_args[0][0]
    assert operations[0]._filter == {"asin": "A1"}
    assert operations[0]._upsert is True


def test_load_reviews_upserts_are_keyed_on_reviewid():
    fake_collection = MagicMock()
    fake_collection.name = "reviews"
    fake_collection.bulk_write.return_value = MagicMock(upserted_count=1, modified_count=0)

    fake_db = {"reviews": fake_collection}
    loader = Loader(fake_db)

    loader.load_reviews([{"reviewID": "R1", "rating": 5}])

    operations = fake_collection.bulk_write.call_args[0][0]
    assert operations[0]._filter == {"reviewID": "R1"}


def test_load_empty_list_skips_bulk_write():
    fake_collection = MagicMock()
    fake_db = {"products": fake_collection}
    loader = Loader(fake_db)

    result = loader.load_products([])

    fake_collection.bulk_write.assert_not_called()
    assert result == 0
