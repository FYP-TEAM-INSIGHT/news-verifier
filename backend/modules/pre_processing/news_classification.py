import requests

# NOTE: Here we hosted in the google colab, the classification is done in the google colab. We use it in here to get the category and subcategory of the news text.


def get_category_subcategory(
    news_text, api_url="https://relaxing-morally-wallaby.ngrok-free.app/check_category"
) -> tuple[str, str]:
    """
    Get the category and subcategory of the news text. This code is hosted in the google colab.
    :param news_text: The text of the news article.
    :param api_url: The URL of the API that performs the classification.
    :return: A tuple containing the category and subcategory of the news article.
    """
    payload = {"text": news_text}
    try:
        response = requests.post(api_url, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return result.get("category", ""), result.get("subcategory", "")
    except Exception as e:
        print(f"[Error] Could not get category and subcategory from API: {e}")
        return "", ""
