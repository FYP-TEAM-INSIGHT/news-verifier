import re

from fastapi import HTTPException

predefined_demo_cases = {
    "ඇන්ජලෝ මැතිව්ස් ටෙස්ට් ක්‍රිකට් වලින් අහක් වෙනවලු": {
        "final_score": 0.91,
        "result": "NOT FAKE ✅",
        "relevant_news": [
            {
                "score": 0.92,
                "link": "https://sinhala.newsfirst.lk/2025/05/23/හිටපු-ශ්‍රී-ලංකා-නායක-අංගෙලෝ",
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


def simulate_news_verification(article_text: str):
    for phrase, result in predefined_demo_cases.items():
        if phrase in article_text:
            return result

    raise HTTPException(
        status_code=400, detail="No matched news found in verified database"
    )
