# mongo-ecommerce-review-analytics

> Status: 🚧 In progress — schema & pipeline setup phase

A MongoDB-backed ingestion and analytics pipeline for e-commerce product and review data.
Built as a standalone project to demonstrate document database schema design (embedding vs.
referencing tradeoffs), PyMongo-driven ETL, and MongoDB aggregation pipeline queries.

## Dataset

[Amazon E-commerce Products & Reviews Dataset](https://www.kaggle.com/datasets/lazylad99/amazon-e-commerce-product-and-review-dataset
) (Kaggle, MIT license)
- `products.csv` — product metadata (brand, price, ratings summary, best-sellers rank, etc.)
- `reviews.csv` — customer reviews linked to products via ASIN, with sentiment scores

Raw data lives in `data/raw/` (see Data section below for why it's tracked this way).

## Planned structure

- [x] Data exploration (`reviews.csv`, `products.csv` done — see `docs/`)
- [x] Schema design doc (embed vs. reference decision, with reasoning — see `docs/schema_design.md`)
- [x] MongoDB running via Docker (Mongo + Mongo Express) — see `docs/screenshots/`
- [x] Schema setup script (collections, validators, indexes — see `src/scripts/setup_schema.py`)
- [ ] Extractor → Transformer → Loader pipeline (PyMongo)
- [ ] 5-8 aggregation pipeline queries answering real analytical questions
- [ ] Error handling + logging throughout
- [ ] Results / findings write-up

## Setup

Local MongoDB via Docker:

```bash
cp .env.example .env   # fill in real values
docker-compose up -d
```

- MongoDB: `localhost:27017`
- Mongo Express (optional web UI): `localhost:8081`

Create the collections, validators, and indexes:

```bash
python src/scripts/setup_schema.py
```

## Tech

- Python, PyMongo
- MongoDB (local/Docker)
- pandas (CSV → dict transformation step)

---
*This README will be rewritten further as the pipeline and aggregation queries are completed.*