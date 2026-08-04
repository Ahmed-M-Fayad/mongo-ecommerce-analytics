# Data

Raw source data for this project. Nothing in this folder is generated — these are the
original files as downloaded, kept as-is so the pipeline's extraction step always has a
known, unmodified starting point.

## Source

**[Amazon E-commerce Products & Reviews Dataset](https://www.kaggle.com/datasets/lazylad99/amazon-e-commerce-product-and-review-dataset)**
— Kaggle, by AlokTheDataGuy
- License: MIT
- Downloaded: August 2026

Described by the author as clothing/accessories product metadata and linked customer
reviews, intended for recommendation systems, sentiment analysis, and e-commerce trend
analysis. Used here for a different purpose — as source data for a MongoDB schema design
and aggregation project — but the underlying data is unchanged.

## Files

### `raw/products.csv`

Product metadata. One row per product. Columns include (non-exhaustive):

- `asin` — unique Amazon product identifier (join key to `reviews.csv`)
- `title`, `brand_name`, `manufacturer`, `model_number`
- `price_value`, `list_price`, `availability`
- `rating_stars`, `rating_count`, `rating_distribution/1star`–`5star`
- `best_sellers_rank`, `recent_purchases`
- `product_description`, `about_item`, `breadcrumbs`
- `all_images`, image/media links
- `seller_name`, `seller_page_url`
- `scrape_time`

### `raw/reviews.csv`

Customer reviews. One row per review, linked to a product via `productASIN`. Columns
include (non-exhaustive):

- `reviewID` — unique review identifier
- `productASIN` — foreign key to `products.csv`'s `asin`
- `rating`, `reviewText`, `reviewTitle`
- `cleaned_review_text`, `sentiment_score` — preprocessed text and a computed sentiment
  score (0–1)
- `verifiedPurchase`, `helpfulVote`
- `productVariant`, `reviewMetadata`, `reviewPosition`
- `images/0`–`images/7`, `videos/0` — mostly null; see note below

## Known data quality notes

Carried over from the source dataset's own field profile, worth knowing before writing the
Extractor/Transformer:

- **Review image/video columns are heavily null** (90–100% null across `images/0`
  through `images/7` and `videos/0`). These are very likely dropped or ignored during
  transformation rather than embedded — a decision to record in `docs/schema_design.md`,
  not silently discard.
- **`reviewPosition` is 0 for the large majority of rows**, with occasional non-zero
  values — worth checking whether this field is actually meaningful before using it in
  any aggregation.
- General expectation: like most scraped e-commerce data, assume some missing values,
  inconsistent string formatting (prices, dates), and duplicate or near-duplicate rows
  until verified during the Transformer step.

