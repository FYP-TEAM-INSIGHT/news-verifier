# Dynamic Ontology Module

## 🧠 What is the Dynamic Ontology Module?
This module manages the ontology (knowledge graph) for news articles. It allows you to add, update, and analyze news data in a structured, machine-readable way using semantic web technologies (OWL/RDF).

## 🚦 How Does It Work? (The Flow)
1. **Initialization**: When the backend starts, the `OntologyManager` loads the ontology file (`new-ontology-v1.owl`). If it doesn't exist, it creates a new one using the schema.
2. **Adding News**: When a news article is submitted (via API), the system:
   - Receives the news data (headline, content, date, source, etc.)
   - Maps each field to the correct ontology property (e.g., `headline` → `hasTitle`, `content` → `hasFullText`)
   - Creates a new `NewsArticle` individual in the ontology
   - Adds related entities (persons, locations, organizations, events) as needed
   - Saves the updated ontology
3. **Bulk Population**: You can also send a batch of news articles. The module processes each one and reports which were successful or failed.
4. **Querying**: The ontology can be queried for statistics (e.g., number of articles, persons, etc.) or for more advanced semantic queries.

## 🗺️ How News Data is Mapped
- **headline** → `hasTitle`
- **content** → `hasFullText`
- **timestamp** → `hasPublicationDate`
- **url** → `hasSourceURL`
- **source** → `publisherName`
- **persons** → `Person` individuals (linked to the article)
- **locations** → `Location` individuals (linked to the article)
- **organizations** → `Organization` individuals (linked to the article)
- **events** → `Event` individuals (linked to the article)

## 🧩 Main Components
- `manager.py`: Loads, saves, and manages the ontology file and its entities.
- `models.py`: Defines the data structures (Pydantic models) for news articles.
- `populator.py`: Contains logic for adding single or multiple news articles to the ontology.
- `schema.py`: Defines the ontology schema (classes and properties).
- `config.py`: Stores configuration like file paths and ontology IRIs.

## 🧩 How News Article Population Works (Detailed Flow)

### 1. Receiving News Data
- The backend receives a news article (or a batch) via API, containing fields like headline, content, timestamp, url, source, category, subcategory, persons, locations, organizations, and events.

### 2. Data Validation & Parsing
- The data is validated using Pydantic models (see `models.py`).
- The timestamp is parsed and normalized to a standard datetime format.

### 3. Article Creation
- A `FormattedNewsArticle` object is created for the core article fields.
- The `OntologyManager.add_article()` method creates a new `NewsArticle` individual in the ontology, mapping fields like headline, content, timestamp, url, and source to ontology properties.

### 4. Category & Subcategory Mapping
- The system looks up the ontology class for the given category and subcategory (e.g., `Sports`, `Cricket`).
- If the class does not exist, an error is raised.
- Category and subcategory individuals are created (if not already present) and linked to the article.

### 5. Entity Extraction & Linking
- For each entity type (persons, locations, organizations, events):
  - The system checks if an individual with the same name exists in the ontology.
  - If not, it creates a new individual for that entity (e.g., a new `Person`).
  - All entities are linked to the article via the `mentionsEntity` property.

### 6. Category/Subcategory-Specific Relationships
- Depending on the category and subcategory, entities are also linked using more specific properties. For example:
  - In `Sports`/`Cricket`, organizations are linked as `hasCricketTeam`, persons as `hasCricketPlayer`, etc.
  - In `PoliticsAndGovernance`/`InternationalPolitics`, organizations are linked as `hasForeignOrganization`, etc.
- This mapping is hardcoded in the logic (see `populator.py`) and ensures rich, semantically meaningful relationships.

### 7. Saving the Ontology
- After all individuals and relationships are created, the ontology is saved to disk.

### 8. Bulk Population
- For bulk operations, each article is processed in sequence.
- Successes and errors are tracked and reported in the API response.

---
### 📝 Example: What Happens When You Populate a News Article
1. You POST a news article to the API.
2. The backend validates and parses the data.
3. The article and all related entities (persons, locations, etc.) are created/linked in the ontology.
4. Category-specific relationships are set (e.g., a cricket player is linked as `hasCricketPlayer`).
5. The ontology is saved, and you get a response with the result.

This process ensures your news data is not just stored, but semantically structured for advanced search, reasoning, and analytics.

---
This module makes your news data semantically rich and ready for advanced reasoning, search, and analysis!
