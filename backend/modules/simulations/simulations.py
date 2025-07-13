import re

mock_news_database = [
    {
        "keywords": ["celebrity", "died", "death", "passed away"],
        "response": {
            "final_score": 0.23,
            "result": "LIKELY FAKE ❌",
            "relevant_news": [
                {
                    "score": 0.15,
                    "link": "https://example.com/celebrity-hoax-debunked",
                },
                {"score": 0.31, "link": "https://example.com/similar-false-claims"},
            ],
            "breakdown": {
                "entity_similarity": 0.45,
                "semantic_similarity": 0.12,
                "source_credibility": 0.1,
                "per_entity": {
                    "persons": 0.2,
                    "locations": 0.85,
                    "events": 0.15,
                    "organizations": 0.3,
                },
            },
        },
    },
    {
        "keywords": ["vaccine", "microchip", "5g", "conspiracy"],
        "response": {
            "final_score": 0.18,
            "result": "FAKE NEWS ❌",
            "relevant_news": [
                {"score": 0.89, "link": "https://example.com/vaccine-facts-who"},
                {
                    "score": 0.76,
                    "link": "https://example.com/debunking-microchip-myth",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.25,
                "semantic_similarity": 0.08,
                "source_credibility": 0.05,
                "per_entity": {
                    "persons": 0.1,
                    "locations": 0.4,
                    "events": 0.12,
                    "organizations": 0.15,
                },
            },
        },
    },
    {
        "keywords": ["election", "fraud", "stolen", "rigged"],
        "response": {
            "final_score": 0.31,
            "result": "LIKELY FAKE ❌",
            "relevant_news": [
                {
                    "score": 0.67,
                    "link": "https://example.com/election-security-report",
                },
                {
                    "score": 0.54,
                    "link": "https://example.com/fact-check-election-claims",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.4,
                "semantic_similarity": 0.28,
                "source_credibility": 0.25,
                "per_entity": {
                    "persons": 0.35,
                    "locations": 0.45,
                    "events": 0.2,
                    "organizations": 0.25,
                },
            },
        },
    },
    {
        "keywords": ["climate", "hoax", "not real", "fake science"],
        "response": {
            "final_score": 0.22,
            "result": "FAKE NEWS ❌",
            "relevant_news": [
                {"score": 0.92, "link": "https://example.com/nasa-climate-data"},
                {"score": 0.88, "link": "https://example.com/ipcc-climate-report"},
            ],
            "breakdown": {
                "entity_similarity": 0.3,
                "semantic_similarity": 0.15,
                "source_credibility": 0.2,
                "per_entity": {
                    "persons": 0.25,
                    "locations": 0.4,
                    "events": 0.18,
                    "organizations": 0.05,
                },
            },
        },
    },
    {
        "keywords": ["breaking", "confirmed", "official", "reuters", "ap news"],
        "response": {
            "final_score": 0.87,
            "result": "NOT FAKE ✅",
            "relevant_news": [
                {
                    "score": 0.91,
                    "link": "https://example.com/reuters-original-story",
                },
                {"score": 0.85, "link": "https://example.com/ap-news-confirmation"},
            ],
            "breakdown": {
                "entity_similarity": 0.92,
                "semantic_similarity": 0.84,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.88,
                    "locations": 0.9,
                    "events": 0.85,
                    "organizations": 0.87,
                },
            },
        },
    },
    {
        "keywords": ["study", "research", "university", "published", "journal"],
        "response": {
            "final_score": 0.79,
            "result": "NOT FAKE ✅",
            "relevant_news": [
                {"score": 0.83, "link": "https://example.com/peer-reviewed-study"},
                {
                    "score": 0.77,
                    "link": "https://example.com/university-press-release",
                },
            ],
            "breakdown": {
                "entity_similarity": 0.85,
                "semantic_similarity": 0.75,
                "source_credibility": 0.88,
                "per_entity": {
                    "persons": 0.82,
                    "locations": 0.78,
                    "events": 0.76,
                    "organizations": 0.85,
                },
            },
        },
    },
]

error_conditions = [
    {
        "keywords": ["hello", "hi", "how are you", "good morning", "good evening"],
        "error": {
            "status": 400,
            "message": "This appears to be a greeting, not news content",
        },
    },
    {
        "keywords": ["recipe", "cooking", "ingredients", "bake", "cook"],
        "error": {
            "status": 400,
            "message": "This appears to be a recipe, not news content",
        },
    },
    {
        "keywords": ["shopping", "buy", "sale", "discount", "price"],
        "error": {
            "status": 400,
            "message": "This appears to be shopping content, not news",
        },
    },
    {
        "keywords": ["love", "relationship", "dating", "romance"],
        "error": {
            "status": 400,
            "message": "This appears to be personal content, not news",
        },
    },
    {
        "keywords": ["test", "testing", "sample", "example"],
        "error": {
            "status": 400,
            "message": "No matched news found in verified database",
        },
    },
]


def simulate_news_verification(article_text: str):
    """Simulate news verification for testing purposes"""

    lower_text = article_text.lower().strip()

    # Check for error conditions first
    from fastapi import HTTPException

    for condition in error_conditions:
        if any(keyword in lower_text for keyword in condition["keywords"]):
            raise HTTPException(
                status_code=condition["error"]["status"],
                detail=condition["error"]["message"],
            )

    # Check if text is too short
    if len(article_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text is too short to analyze. Please provide more content.",
        )

    # Check if text is just numbers or symbols
    if not re.search(r"[a-zA-Z]", article_text):
        raise HTTPException(
            status_code=400,
            detail="Invalid content format. Please provide readable news text.",
        )

    # Find matching response based on keywords
    for item in mock_news_database:
        if any(keyword in lower_text for keyword in item["keywords"]):
            return item["response"]

    # Default response for unmatched text (neutral/credible)
    return {
        "final_score": 0.65,
        "result": "NEEDS VERIFICATION ⚠️",
        "relevant_news": [
            {"score": 0.45, "link": "https://example.com/similar-topic-1"},
            {"score": 0.38, "link": "https://example.com/related-news-2"},
        ],
        "breakdown": {
            "entity_similarity": 0.7,
            "semantic_similarity": 0.6,
            "source_credibility": 0.65,
            "per_entity": {
                "persons": 0.68,
                "locations": 0.72,
                "events": 0.58,
                "organizations": 0.63,
            },
        },
    }
