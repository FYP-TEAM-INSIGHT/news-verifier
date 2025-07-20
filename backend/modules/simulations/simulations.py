from sinling import SinhalaTokenizer
from fastapi import HTTPException

tokenizer = SinhalaTokenizer()


demo_cases = [
    {
        "keyword": ["ඇන්ජලෝ", "මැතිව්ස්", "ටෙස්ට්", "ක්‍රිකට්"],
        "result": {
            "final_score": 0.91,
            "result": "NOT FAKE ✅",
            "semantic_ranking": [
                {
                    "score": 0.96,
                    "title": "හිටපු ශ්‍රී ලංකා නායක ඇන්ජලෝ මැතිව්ස් ටෙස්ට් ක්‍රිකට් පිටියට සමු දෙන බවට නිවේදනය කරයි",
                    "url": "https://sinhala.newsfirst.lk/2025/05/23/%e0%b7%84%e0%b7%92%e0%b6%a7%e0%b6%b4%e0%b7%94-%e0%b7%81%e0%b7%8a%e2%80%8d%e0%b6%bb%e0%b7%93-%e0%b6%bd%e0%b6%82%e0%b6%9a%e0%b7%8f-%e0%b6%b1%e0%b7%8f",
                }
            ],
            "breakdown": {
                "entity_similarity": 0.93,
                "semantic_similarity": 0.87,
                "source_credibility": 0.95,
                "per_entity": {
                    "persons": 0.9,
                    "locations": 0.8,
                    "events": 0.92,
                    "organizations": 0.5,
                },
            },
        },
    }
]


def simulate_news_verification(article_text: str):
    tokens = tokenizer.tokenize(article_text)
    max_match_count = 0
    best_case = None

    for case in demo_cases:
        match_count = sum(1 for keyword in case["keyword"] if keyword in tokens)
        if match_count > max_match_count:
            max_match_count = match_count
            best_case = case

    if best_case and max_match_count > 0:
        return best_case["result"]

    raise HTTPException(
        status_code=400, detail="No matched news found in verified database"
    )
