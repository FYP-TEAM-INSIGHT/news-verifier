import requests

# NOTE: Here we hosted in the google colab, the classification is done in the google colab. We use it in here to get the category and subcategory of the news text.


def get_category_subcategory(
    news_text, api_url="https://relaxing-morally-wallaby.ngrok-free.app/check_category"
):
    payload = {"text": news_text}
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("category", ""), result.get("subcategory", "")
    except Exception as e:
        print(f"[Error] Could not get category and subcategory from API: {e}")
        return "", ""
