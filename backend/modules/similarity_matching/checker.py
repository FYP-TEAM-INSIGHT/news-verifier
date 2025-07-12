"""
Main entry point for fake news similarity checking logic.
"""

from typing import Dict, Any
from .similarity_engine import (
    get_verified_values,
    get_trusted_publishers,
    get_source_credibility,
    get_trusted_contents_by_category,
    get_semantic_similarity_score,
    get_average_similarity,
)
from .query_mapping import QUERY_MAP


def check_fake(
    news_json: Dict[str, Any], ontology_manager, debug: bool = False
) -> Dict[str, Any]:
    """
    Checks if a news article is fake by comparing entities, content, and source credibility.
    Returns a score, result label, and breakdown.
    """
    subcat = news_json.get("subcategory")
    entity_types = ["persons", "locations", "events", "organizations"]

    avg_scores = {}
    debug_outputs = {}
    counts = {}
    total_weight = 0
    weighted_sum = 0

    for etype in entity_types:
        values = news_json.get(etype, [])
        counts[etype] = len(values)
        if subcat in QUERY_MAP and etype in QUERY_MAP[subcat]:
            verified = get_verified_values(QUERY_MAP[subcat][etype])
        else:
            verified = []
        avg, debug_pairs = get_average_similarity(
            values, verified, etype if debug else None
        )
        avg_scores[etype] = avg
        debug_outputs[etype] = debug_pairs
        weighted_sum += avg * counts[etype]
        total_weight += counts[etype]

    entity_similarity_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    if debug:
        print("\n[Entity Similarity] Average scores per entity type:")
        for etype, score in avg_scores.items():
            print(f"  {etype}: {score:.3f} (count={counts[etype]})")
        print(f"  Overall entity similarity score: {entity_similarity_score:.3f}")

    # --- Semantic Similarity ---
    trusted_texts = get_trusted_contents_by_category(subcat)
    content = news_json.get("content", "")
    semantic_similarity_score = get_semantic_similarity_score(content, trusted_texts)
    if debug:
        print(f"\n[Semantic Similarity] Content: {content!r}")
        print(f"  Trusted texts: {trusted_texts[:3]}... (total {len(trusted_texts)})")
        print(f"  Semantic similarity score: {semantic_similarity_score:.3f}")

    # --- Source Credibility ---
    trusted_publishers = get_trusted_publishers()
    publisher = news_json.get("source", "")
    source_credibility_score = get_source_credibility(publisher, trusted_publishers)

    if debug:
        print(f"\n[Source Credibility] Publisher: {publisher!r}")
        print(
            f"  Trusted publishers: {trusted_publishers[:3]}... (total {len(trusted_publishers)})"
        )
        print(f"  Source credibility score: {source_credibility_score:.3f}")

    # --- Composite Score (weights can be tuned, e.g. 0.4/0.3/0.3) ---
    final_score = (
        0.4 * entity_similarity_score
        + 0.3 * semantic_similarity_score
        + 0.3 * source_credibility_score
    )

    # Result label based on your new rules
    if final_score >= 0.7:
        result = "NOT FAKE ✅"
    elif final_score >= 0.4:
        result = "MIGHT BE FAKE ⚠️"
    else:
        result = "POSSIBLY FAKE ❌"

    return {
        "final_score": round(final_score, 3),
        "result": result,
        "breakdown": {
            "entity_similarity": entity_similarity_score,
            "semantic_similarity": semantic_similarity_score,
            "source_credibility": source_credibility_score,
            "per_entity": avg_scores,
        },
    }
