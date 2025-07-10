from requests import post
from requests.exceptions import RequestException
from pydantic import BaseModel


class NERServiceOutput(BaseModel):
    persons: list[str]
    locations: list[str]
    organizations: list[str]
    events: list[str]


def extract_named_entities(
    text: str, api_url="https://ner-server-v2.onrender.com"
) -> NERServiceOutput:
    """
    Extract named entities from the given text using an external NER service.

    Args:
        text (str): The input text from which to extract named entities.
        api_url (str): The URL of the NER service.

    Returns:
        NERServiceOutput: The extracted named entities as a Pydantic model.
    """
    payload = {"text": text}
    try:
        response = post(api_url, json=payload, timeout=90)
        response.raise_for_status()
        return NERServiceOutput(**response.json())
    except RequestException as e:
        raise Exception(f"Failed to extract named entities: {e}")
