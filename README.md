# mongo-ecommerce-review-analytics

> Status: 🚧 In progress — schema design phase

A MongoDB-backed ingestion and analytics pipeline for e-commerce product and review data.
Built as a standalone project to demonstrate document database schema design (embedding vs.
referencing tradeoffs), PyMongo-driven ETL, and MongoDB aggregation pipeline queries.

## Dataset

[Amazon E-commerce Products & Reviews Dataset](https://www.kaggle.com/datasets/aloktheDataGuy/amazon-e-commerce-products-and-reviews-dataset) (Kaggle, MIT license)
- `products.csv` — product metadata (brand, price, ratings summary, best-sellers rank, etc.)
- `reviews.csv` — customer reviews linked to products via ASIN, with sentiment scores

Raw data lives in `data/raw/` (see Data section below for why it's tracked this way).

## Why this project

Built after completing MongoDB fundamentals + PyMongo study, to fix the concepts by building
something real rather than just running the lab assignment. Core goal: make a deliberate,
documented schema design decision (what to embed vs. what to reference) and justify it —
not just dump both CSVs into collections.

## Planned structure

- [ ] Schema design doc (embed vs. reference decisions, with reasoning)
- [ ] Extractor → Transformer → Loader pipeline (PyMongo)
- [ ] Indexes justified by actual query patterns
- [ ] 5-8 aggregation pipeline queries answering real analytical questions
- [ ] Error handling + logging throughout
- [ ] Results / findings write-up

## Setup

_TBD once pipeline code exists — will include Docker/Mongo connection instructions._

## Tech

- Python, PyMongo
- MongoDB (local/Docker)
- pandas (CSV → dict transformation step)

---
*This README is a placeholder and will be rewritten once the schema design and pipeline are complete.*
