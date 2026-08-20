"""Runs the project's aggregation queries against the reviews and products collections."""


def top_rated_products(db, min_reviews=5, limit=5):
    """Q1: top N products by average rating, with at least min_reviews reviews."""
    pipeline = [
        {"$group": {"_id": "$productASIN", "avg_rating": {"$avg": "$rating"}, "review_count": {"$sum": 1}}},
        {"$match": {"review_count": {"$gte": min_reviews}}},
        {"$sort": {"avg_rating": -1}},
        {"$limit": limit},
        {"$lookup": {"from": "products", "localField": "_id", "foreignField": "asin", "as": "product"}},
        {"$unwind": "$product"},
        {"$project": {"_id": 0, "asin": "$_id", "title": "$product.title", "avg_rating": 1, "review_count": 1}},
    ]
    return list(db["reviews"].aggregate(pipeline))


def verified_vs_unverified(db):
    """Q2: average rating and sentiment score, split by verifiedPurchase."""
    pipeline = [
        {"$match": {"rating": {"$ne": None}, "sentiment_score": {"$ne": None}}},
        {"$group": {
            "_id": "$verifiedPurchase",
            "avg_rating": {"$avg": "$rating"},
            "avg_sentiment": {"$avg": "$sentiment_score"},
        }},
    ]
    return list(db["reviews"].aggregate(pipeline))


def biggest_rating_sentiment_gap(db, limit=5):
    """Q3: products where star rating and text sentiment disagree the most."""
    pipeline = [
        {"$match": {"rating": {"$ne": None}, "sentiment_score": {"$ne": None}}},
        {"$addFields": {
            "rating_norm": {"$divide": [{"$subtract": ["$rating", 3]}, 2]},
        }},
        {"$addFields": {
            "gap": {"$abs": {"$subtract": ["$rating_norm", "$sentiment_score"]}},
        }},
        {"$group": {"_id": "$productASIN", "avg_gap": {"$avg": "$gap"}}},
        {"$sort": {"avg_gap": -1}},
        {"$limit": limit},
        {"$lookup": {"from": "products", "localField": "_id", "foreignField": "asin", "as": "product"}},
        {"$unwind": "$product"},
        {"$project": {"_id": 0, "asin": "$_id", "title": "$product.title", "avg_gap": 1}},
    ]
    return list(db["reviews"].aggregate(pipeline))


def avg_price_by_category(db, limit=5):
    """Q4: average price_value grouped by the top-level product category."""
    pipeline = [
        {"$addFields": {"category_top": {"$arrayElemAt": ["$category", 0]}}},
        {"$match": {"category_top": {"$ne": None}, "price_value": {"$ne": None}}},
        {"$group": {"_id": "$category_top", "avg_price": {"$avg": "$price_value"}}},
        {"$sort": {"avg_price": -1}},
        {"$limit": limit},
    ]
    return list(db["products"].aggregate(pipeline))


def helpful_votes_by_image_presence(db):
    """Q5: average helpfulVoteCount, split by whether the review has any images."""
    pipeline = [
        {"$addFields": {"has_image": {"$gt": [{"$size": {"$ifNull": ["$images", []]}}, 0]}}},
        {"$group": {"_id": "$has_image", "avg_helpful_votes": {"$avg": "$helpfulVoteCount"}}},
    ]
    return list(db["reviews"].aggregate(pipeline))


def products_with_zero_reviews(db):
    """Q6: count of products that have no matching review documents."""
    pipeline = [
        {"$lookup": {"from": "reviews", "localField": "asin", "foreignField": "productASIN", "as": "reviews"}},
        {"$match": {"reviews": {"$size": 0}}},
        {"$count": "zero_review_products"},
    ]
    result = list(db["products"].aggregate(pipeline))
    return result[0]["zero_review_products"] if result else 0


def run_all(db):
    """Run every query and return the results as a dict, keyed by question."""
    return {
        "top_rated_products": top_rated_products(db),
        "verified_vs_unverified": verified_vs_unverified(db),
        "biggest_rating_sentiment_gap": biggest_rating_sentiment_gap(db),
        "avg_price_by_category": avg_price_by_category(db),
        "helpful_votes_by_image_presence": helpful_votes_by_image_presence(db),
        "products_with_zero_reviews": products_with_zero_reviews(db),
    }


if __name__ == "__main__":
    from db import get_db

    client, db = get_db()
    results = run_all(db)
    for question, answer in results.items():
        print(f"\n--- {question} ---")
        print(answer)
    client.close()