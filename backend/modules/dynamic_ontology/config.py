"""
Central place for constants so you don't repeat literals across modules.
"""

from pathlib import Path

ONTOLOGY_IRI: str = (
    "http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1"
)

# Updated path to point to the ontology file in the root of ontology-sinhala
ONTOLOGY_FILE: Path = Path(__file__).parent.parent.parent / "new-ontology-v1.owl"
