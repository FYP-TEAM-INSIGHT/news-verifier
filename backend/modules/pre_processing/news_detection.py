from fastapi import HTTPException
import requests


def get_news_or_not(
    news_text, api_url="https://relaxing-morally-wallaby.ngrok-free.app/check_news"
):
    payload = {"text": news_text}
    try:
        response = requests.post(api_url, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return result.get("checking", "")
    except Exception as e:
        print(f"[Error] Could not get news or not from API: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to connect to the news detection service. Please try again later.",
        )
