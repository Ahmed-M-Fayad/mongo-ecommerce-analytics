"""Runs the full pipeline: Extract -> Transform -> Load."""

from db import get_db
from extractor import Extractor
from transformer import Transformer
from loader import Loader

DATA_DIR = "data/raw"


def main():
    client, db = get_db()

    extractor = Extractor(DATA_DIR)
    transformer = Transformer()
    loader = Loader(db)

    products_df = extractor.extract_products()
    reviews_df = extractor.extract_reviews()
    print(f"Extracted {len(products_df)} products, {len(reviews_df)} reviews")

    products_docs = transformer.transform_products(products_df)
    reviews_docs = transformer.transform_reviews(reviews_df)
    print(f"Transformed {len(products_docs)} products, {len(reviews_docs)} reviews")

    products_loaded = loader.load_products(products_docs)
    reviews_loaded = loader.load_reviews(reviews_docs)
    print(f"Loaded {products_loaded} products, {reviews_loaded} reviews")

    client.close()


if __name__ == "__main__":
    main()
