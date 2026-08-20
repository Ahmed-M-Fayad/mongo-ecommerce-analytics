"""Tests for the Transformer's cleaning/parsing helper methods."""

import sys

sys.path.insert(0, "../src")

from transformer import Transformer

t = Transformer()


def test_clean_brand_name_strips_store_suffix():
    assert t._clean_brand_name("Nike Store") == "Nike"


def test_clean_brand_name_strips_brand_prefix():
    assert t._clean_brand_name("Brand: Adidas") == "Adidas"


def test_clean_brand_name_unknown_becomes_none():
    assert t._clean_brand_name("Unknown") is None


def test_clean_brand_name_handles_missing_value():
    assert t._clean_brand_name(None) is None


def test_parse_list_price_extracts_amount():
    assert t._parse_list_price("List Price: $49.99") == 49.99


def test_parse_rating_stars_extracts_number():
    assert t._parse_rating_stars("4.6 out of 5 stars") == 4.6


def test_parse_rating_count_strips_commas():
    assert t._parse_rating_count("1,654 ratings") == 1654


def test_parse_recent_purchases_handles_k_suffix():
    assert t._parse_recent_purchases("1K+ bought") == 1000


def test_parse_recent_purchases_handles_plain_number():
    assert t._parse_recent_purchases("100+ bought") == 100


def test_parse_review_location_extracts_location():
    value = "Reviewed in the United States on March 5, 2025"
    assert t._parse_review_location(value) == "the United States"


def test_parse_image_list_parses_python_list_string():
    value = "['https://a.jpg', 'https://b.jpg']"
    assert t._parse_image_list(value) == ["https://a.jpg", "https://b.jpg"]


def test_parse_image_list_handles_missing_value():
    assert t._parse_image_list(None) == []


def test_normalize_availability_lowercases():
    assert t._normalize_availability("In Stock") == t._normalize_availability("In stock")


def test_to_float_returns_none_for_invalid_value():
    assert t._to_float("not a number") is None


def test_to_int_returns_none_for_invalid_value():
    assert t._to_int(None) is None
