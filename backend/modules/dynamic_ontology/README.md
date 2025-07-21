

# DYNAMIC_ONTOLOGY_MODULE_CONTEXT

## MODULE_PURPOSE
- Implements a dynamic ontology system for news article ingestion, entity extraction, semantic mapping, and knowledge graph population.
- All logic is designed for extensibility and LLM-driven future improvements.

## FILES_AND_ROLES
- `config.py`: Contains ontology IRI, file paths, and configuration constants.
- `manager.py`: OntologyManager class. Handles ontology file load/save, entity CRUD, and graph-level operations.
- `models.py`: Pydantic models for input validation and internal data representation (news article, entities, etc).
- `populator.py`: Core logic for mapping input data to ontology, entity linking, category/subcategory-specific relationships, and batch operations.
- `schema.py`: Ontology schema definition (OWL classes, properties, relationships).
- `README.md`: (this file) - context for LLMs.

## DATA_FLOW
1. **Input**: Receives news article(s) with fields: headline, content, timestamp, url, source, category, subcategory, persons, locations, organizations, events.
2. **Validation**: Uses Pydantic models to validate and normalize input.
3. **Ontology Mapping**:
   - Maps fields to ontology properties:
     - headline → hasTitle
     - content → hasFullText
     - timestamp → hasPublicationDate
     - url → hasSourceURL
     - source → publisherName
   - Entities (persons, locations, organizations, events) are created/linked as individuals.
   - Category/subcategory mapped to ontology classes; if missing, error is raised.
   - Category/subcategory-specific relationships are hardcoded (e.g., hasCricketPlayer, hasForeignOrganization).
   - All entities linked to article via mentionsEntity and specific properties.
4. **Persistence**: Ontology is saved to disk after each operation.
5. **Bulk Operations**: Batch ingestion supported; tracks per-article success/failure.

## SEMANTIC DESIGN
- Ontology is OWL/RDF-based, designed for semantic web compatibility.
- Supports advanced SPARQL queries and reasoning.
- All relationships are explicit; no implicit inference logic in code.

## EXTENSIBILITY
- All mapping logic is centralized in populator.py for easy LLM-driven modification.
- Schema is modular; new entity types, properties, or relationships can be added by extending schema.py and updating mapping logic.
- Designed for future LLMs to:
  - Add new categories/subcategories.
  - Refine entity extraction/linking.
  - Enhance relationship mapping.
  - Integrate with external ontologies.

## EXAMPLES (PSEUDOCODE)
- Input: {headline, content, timestamp, url, source, category, subcategory, persons, locations, organizations, events}
- Output: Ontology file with NewsArticle individual, linked entities, and all relationships.

## NON-HUMAN NOTES
- All logic is explicit; no hidden assumptions.
- All mappings, relationships, and schema elements are discoverable via code inspection.
- Designed for LLMs to parse, understand, and extend with minimal ambiguity.

### Mapping Structure Example

The mapping from (category, subcategory, entity type) to relationship property is typically implemented as a nested dictionary in `populator.py`. Example pseudocode:

```python
RELATIONSHIP_MAPPING = {
  ("Sports", "Cricket", "person"): "hasCricketPlayer",
  ("Sports", "Cricket", "organization"): "hasCricketTeam",
  ("PoliticsAndGovernance", "InternationalPolitics", "organization"): "hasForeignOrganization",
  # ... more mappings ...
}
```

When populating the ontology, the system looks up the property using the article's category, subcategory, and entity type. If a mapping is missing, a default or generic property (e.g., `mentionsEntity`) is used, and optionally a warning is logged.

### Extending or Modifying the Mapping

- To add a new context-aware relationship, insert a new entry in the mapping structure in `populator.py`.
- Ensure the new property is defined in `schema.py` and is consistent with the ontology's design.
- Update any relevant documentation or tests to reflect the new relationship.

### Error Handling and Fallbacks

- If a (category, subcategory, entity type) combination is not found in the mapping, the system falls back to a generic property (e.g., `mentionsEntity`).
- Optionally, a warning or error can be logged for missing mappings to aid debugging and ontology completeness.

### Schema Reference

- All relationship types (properties) used in context-aware mapping are defined in `schema.py`.
- Any new property added to the mapping must also be declared in the schema for consistency and reasoning support.
## CONTEXT-AWARE RELATIONSHIPS

This ontology design supports context-aware relationships, enabling dynamic and semantically rich connections between entities based on the specific context of each news article. The mapping logic in `populator.py` determines which relationships to instantiate according to the article's category, subcategory, and extracted entities. Key features:

- **Dynamic Property Assignment**: Relationships between articles and entities (persons, organizations, locations, events) are not static. The type of relationship (e.g., `hasCricketPlayer`, `hasForeignOrganization`, `hasEventParticipant`) is selected based on the article's semantic context.
- **Category/Subcategory Sensitivity**: For each (category, subcategory) pair, a unique set of properties may be used to link entities. For example:
  - In `Sports`/`Cricket`, persons are linked as `hasCricketPlayer`, organizations as `hasCricketTeam`.
  - In `PoliticsAndGovernance`/`InternationalPolitics`, organizations may be linked as `hasForeignOrganization`.
- **MentionsEntity Backbone**: All entities are also linked via a generic `mentionsEntity` property, ensuring a baseline of connectivity for reasoning and search.
- **Extensible Mapping**: The mapping from (category, subcategory, entity type) to relationship property is hardcoded but modular, allowing LLMs or developers to add new context-aware relationships by updating a single mapping structure.
- **No Implicit Inference**: All context-aware relationships are explicit in the ontology; no relationships are assumed or inferred unless directly instantiated by the mapping logic.

This approach enables the ontology to capture nuanced, context-dependent semantics, supporting advanced reasoning, analytics, and future LLM-driven enhancements.
