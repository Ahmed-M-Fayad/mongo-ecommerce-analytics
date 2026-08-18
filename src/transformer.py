"""Cleans and reshapes raw product/review rows into the document schema from schema_design.md."""

import ast
import re

import pandas as pd


class Transformer:
    """Turns raw products/reviews DataFrames into lists of Mongo-ready documents."""

    def transform_products(self, df):
        """Clean and reshape the products DataFrame into a list of documents."""
        documents = []
        for _, row in df.iterrows():
            try:
                documents.append(self._build_product_doc(row))
            except Exception as e:
                print(f"Skipping product row (asin={row.get('asin')}): {e}")
        return documents

    def transform_reviews(self, df):
        """Clean and reshape the reviews DataFrame into a list of documents."""
        documents = []
        for _, row in df.iterrows():
            try:
                documents.append(self._build_review_doc(row))
            except Exception as e:
                print(f"Skipping review row (reviewID={row.get('reviewID')}): {e}")
        return documents

    def _build_product_doc(self, row):
        """Build a single product document from a raw row."""
        return {
            "asin": row["asin"],
            "title": row["title"],
            "about_item": self._clean_text(row.get("about_item")),
            "product_description": self._clean_text(row.get("product_description")),
            "brand_name": self._clean_brand_name(row.get("brand_name")),
            "manufacturer": self._clean_text(row.get("manufacturer")),
            "model_number": self._clean_text(row.get("model_number")),
            "availability": self._normalize_availability(row.get("availability")),
            "price_value": self._to_float(row.get("price_value")),
            "list_price": self._parse_list_price(row.get("list_price")),
            "product_url": row.get("product_url"),
            "images": self._parse_image_list(row.get("all_images")),
            "seller_name": self._clean_text(row.get("seller_name")),
            "category": self._parse_category(row.get("breadcrumbs")),
            "rank": self._to_int(row.get("rank_1")),
            "variants": self._build_variants(row),
            "rating_snapshot": {
                "rating_stars": self._parse_rating_stars(row.get("rating_stars")),
                "rating_count": self._parse_rating_count(row.get("rating_count")),
                "rating_distribution": self._build_rating_distribution(row),
                "recent_purchases": self._parse_recent_purchases(row.get("recent_purchases")),
                "as_of": row.get("scrape_time"),
            },
        }

    def _build_review_doc(self, row):
        """Build a single review document from a raw row."""
        return {
            "reviewID": row["reviewID"],
            "productASIN": row["productASIN"],
            "rating": self._to_float(row.get("rating")),
            "reviewTitle": self._clean_text(row.get("reviewTitle")),
            "reviewText": self._clean_text(row.get("reviewText")),
            "cleaned_review_text": self._clean_text(row.get("cleaned_review_text")),
            "sentiment_score": self._to_float(row.get("sentiment_score")),
            "verifiedPurchase": bool(row.get("verifiedPurchase")),
            "helpfulVoteCount": self._to_int(row.get("helpfulVoteCount")),
            "reviewPosition": self._to_int(row.get("reviewPosition")),
            "reviewURL": row.get("reviewURL"),
            "location": self._parse_review_location(row.get("reviewMetadata")),
            "images": [row[c] for c in row.index if c.startswith("images/") and pd.notna(row[c])],
        }

    def _clean_text(self, value):
        """Return None for NaN/empty text, otherwise the stripped string."""
        if pd.isna(value):
            return None
        return str(value).strip()

    def _to_float(self, value):
        """Convert a value to float, returning None if it isn't a valid number."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _to_int(self, value):
        """Convert a value to int, returning None if it isn't a valid number."""
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None

    def _normalize_availability(self, value):
        """Collapse inconsistent capitalization (e.g. 'In stock' vs 'In Stock')."""
        if pd.isna(value):
            return None
        return str(value).strip().lower()

    def _clean_brand_name(self, value):
        """Strip 'Store'/'Brand:' noise and normalize 'Unknown' to None."""
        if pd.isna(value):
            return None
        name = str(value).strip()
        if name.lower() == "unknown":
            return None
        name = re.sub(r"\s*Store$", "", name)
        name = re.sub(r"^Brand:\s*", "", name)
        return name.strip()

    def _parse_list_price(self, value):
        """Extract the numeric amount from a 'List Price: $X' string."""
        if pd.isna(value):
            return None
        match = re.search(r"[\d.]+", str(value))
        return float(match.group()) if match else None

    def _parse_image_list(self, value):
        """Parse the stringified Python list in all_images into a real list."""
        if pd.isna(value):
            return []
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            print(f"Could not parse all_images value: {value}")
            return []

    def _parse_category(self, value):
        """Extract the category trail from the breadcrumbs '›'-separated string."""
        if pd.isna(value):
            return None
        return [part.strip() for part in str(value).split("›")]

    def _build_variants(self, row):
        """Collect the non-null default_variant/N values into a list."""
        cols = ["default_variant/0", "default_variant/1", "default_variant/2"]
        return [row[c] for c in cols if c in row.index and pd.notna(row[c])]

    def _parse_rating_stars(self, value):
        """Extract the numeric rating from a '4.6 out of 5 stars' string."""
        if pd.isna(value):
            return None
        match = re.search(r"[\d.]+", str(value))
        return float(match.group()) if match else None

    def _parse_rating_count(self, value):
        """Extract the numeric count from a '1,654 ratings' string."""
        if pd.isna(value):
            return None
        digits = re.sub(r"[^\d]", "", str(value))
        return int(digits) if digits else None

    def _build_rating_distribution(self, row):
        """Collect the rating_distribution/Nstar columns into one dict."""
        distribution = {}
        for n in range(1, 6):
            col = f"rating_distribution/{n}star"
            if col in row.index and pd.notna(row[col]):
                digits = re.sub(r"[^\d]", "", str(row[col]))
                distribution[f"{n}star"] = int(digits) if digits else None
        return distribution

    def _parse_recent_purchases(self, value):
        """Extract the numeric floor from a '100+ bought'/'1K+ bought' string."""
        if pd.isna(value):
            return None
        match = re.search(r"([\d.]+)(K)?", str(value))
        if not match:
            return None
        number = float(match.group(1))
        if match.group(2) == "K":
            number *= 1000
        return int(number)

    def _parse_review_location(self, value):
        """Extract the location from a 'Reviewed in <location> on <date>' string."""
        if pd.isna(value):
            return None
        match = re.search(r"Reviewed in (.+?) on", str(value))
        return match.group(1) if match else None
