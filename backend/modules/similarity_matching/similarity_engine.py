"""
Algorithms for string/entity/semantic similarity.
"""

from pydantic import BaseModel
import requests
from rapidfuzz.fuzz import ratio
from owlready2 import default_world

# 1. Helper: Get verified values from ontology using SPARQL


class TrustedContent(BaseModel):
    trustSementics: str
    title: str
    url: str


def get_verified_values(sparql_query):
    results = list(default_world.sparql(sparql_query))
    return [str(item[0]) for item in results]


def get_trusted_publishers():
    sparql = """
    PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>
    SELECT DISTINCT ?publisher
    WHERE {
      ?article ns:publisherName ?publisher .
    }
    """
    results = list(default_world.sparql(sparql))
    return [str(r[0]) for r in results]


def get_source_credibility(news_publisher, trusted_publishers):
    # return 1.0 if news_publisher in trusted_publishers else 0.0
    return 1.0  # we need to update logic later to use trusted publishers


def get_trusted_contents_by_category(category):
    category_uri = f"ns:{category}"
    sparql = f"""
    PREFIX ns: <http://www.semanticweb.org/kingmalitha/ontologies/2025/5/new-ontology-v1#>
    SELECT DISTINCT ?trustSementics ?title ?url
    WHERE {{
      ?article ns:hasCategory ?cat .
      FILTER (?cat = {category_uri})
      ?article ns:hasFullText ?trustSementics .
      ?article ns:hasTitle ?title .
      ?article ns:hasSourceURL ?url .
    }}
    """
    results = list(default_world.sparql(sparql))
    return [
        TrustedContent(trustSementics=str(r[0]), title=str(r[1]), url=str(r[2]))
        for r in results
    ]


def get_semantic_similarity_score(
    news_text,
    trusted_texts,
    api_url="https://relaxing-morally-wallaby.ngrok-free.app/similarity",
):
    payload = {"news_text": news_text, "trusted_texts": trusted_texts}
    try:
        response = requests.post(api_url, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return float(result.get("max_similarity", 0.0))
    except Exception as e:
        print(f"[Error] Could not get similarity from API: {e}")
        return 0.0


def get_average_similarity(input_list, verified_list, debug_label=None):
    if not input_list:
        return 1.0, []
    total = 0
    debug_pairs = []
    for value in input_list:
        if verified_list:
            scores = [ratio(value, v) for v in verified_list]
            max_score = max(scores)
            best_match = verified_list[scores.index(max_score)]
        else:
            max_score = 0
            best_match = None
        total += max_score / 100.0
        debug_pairs.append((value, best_match, max_score / 100.0))
    if debug_label:
        print(f"\n[{debug_label}] Best matches:")
        for val, match, scr in debug_pairs:
            print(f"  Input: {val!r} --> Ontology: {match!r} (score={scr:.2f})")
    return total / len(input_list), debug_pairs
