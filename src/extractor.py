"""Reads the raw product and review CSVs into DataFrames. Does no transformation."""

import pandas as pd


class Extractor:
    """Loads products.csv and reviews.csv from a given data directory."""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def extract_products(self):
        """Read products.csv and return it as a DataFrame."""
        path = f"{self.data_dir}/products.csv"
        try:
            return pd.read_csv(path, low_memory=False)
        except FileNotFoundError:
            print(f"products.csv not found at {path}")
            raise
        except pd.errors.EmptyDataError:
            print("products.csv is empty")
            raise

    def extract_reviews(self):
        """Read reviews.csv and return it as a DataFrame."""
        path = f"{self.data_dir}/reviews.csv"
        try:
            return pd.read_csv(path, low_memory=False)
        except FileNotFoundError:
            print(f"reviews.csv not found at {path}")
            raise
        except pd.errors.EmptyDataError:
            print("reviews.csv is empty")
            raise
