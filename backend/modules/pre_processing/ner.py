import requests
from requests.exceptions import RequestException
from pydantic import BaseModel


class NERServiceOutput(BaseModel):
    persons: list[str]
    locations: list[str]
    organizations: list[str]
    events: list[str]


def extract_named_entities(news_text, api_url="https://ner-server-v2.onrender.com/ner"):
    payload = {"text": news_text}
    try:
        response = requests.post(api_url, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return (
            result.get("persons", []),
            result.get("locations", []),
            result.get("events", []),
            result.get("organizations", []),
        )
    except Exception as e:
        print(f"[Error] Could not get entities from API: {e}")
        return [], [], [], []
