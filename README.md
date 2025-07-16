# Sinhala News Ontology System

A semantic knowledge representation system for Sinhala news articles that structures unstructured news content into a formal ontology for automated analysis and fact verification.

## 📖 Overview

This project creates a comprehensive ontology (knowledge graph) specifically designed for Sinhala news content. It automatically categorizes news articles, extracts named entities (people, places, organizations, events), and structures this information in a machine-readable format that can be used for fact-checking and news verification.

## 🎯 Purpose

The main objectives of this system are:

- **Automated News Classification**: Categorize Sinhala news into domains like Politics, Sports, Crime, etc.
- **Named Entity Recognition**: Extract and link people, places, organizations, and events mentioned in news
- **Semantic Relationships**: Establish meaningful connections between entities and news categories
- **Fact Verification Support**: Provide structured data for automated fact-checking systems
- **Knowledge Graph Generation**: Create a queryable knowledge base of Sinhala news content


## 📂 Project Structure

```
backend/
frontend/
```

## 🛠️ Installation

To set up the backend environment for the Sinhala News Ontology System, follow these steps:

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the news-verifier directory:

```bash
cd news-verifier
```

3. Docker compose up 
```bash
docker compose up -d
```

### How to run the backend only

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:
```bash
source .venv/Scripts/activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the backend server:

```bash
python main.py
```

Note: Ensure you have Python 3.8+ installed and the necessary permissions to run the server. Also you need to change the running host because, it is used 0.0.0.0, but in windows it is not working, so you need to change it to 127.0.0.1
```py
    # WHEN RUNNING ON DOCKER
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

    # LOCAL DEVELOPMENT ON 127.0.0.1 (SPECIALLY ON WINDOWS)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
```

## 🏗️ System Architecture

### Core Components

#### 1. **Schema Definition** (`ontology_sinhala/schema.py`)

- Defines the ontology vocabulary and class hierarchy
- Creates relationships between news categories and entities
- Supports 5 main news categories:
  - **Politics & Governance** (International/Domestic)
  - **Science & Technology** (Tech/Research)
  - **Culture & Entertainment** (Screen/Music)
  - **Sports** (Cricket/Football/Other)
  - **Crime & Justice** (Crime Reports/Courts)

#### 2. **Ontology Manager** (`ontology_sinhala/manager.py`)

- Handles ontology creation and loading
- Manages saving/loading from OWL files
- Provides safe name generation for Sinhala text
- Creates article instances with metadata

#### 3. **Data Models** (`ontology_sinhala/models.py`)

- Defines structured data containers for news articles
- Ensures type safety and data validation

#### 4. **Content Populator** (`ontology_sinhala/ontology_populator.py`)

- Processes JSON news data into ontology instances
- Maps entities to appropriate categories and subcategories
- Creates semantic relationships between articles and entities

#### 5. **Configuration** (`ontology_sinhala/config.py`)

- Centralized configuration for ontology IRI and file paths
- Maintains consistent naming conventions

## 🚀 Getting Started

### Prerequisites

```bash
pip install owlready2
```

### Basic Usage

1. **Initialize the Ontology System**:

```python
from ontology_sinhala.manager import OntologyManager
manager = OntologyManager()
```

2. **Add News Articles**:

```python
from ontology_sinhala.ontology_populator import populate_article_from_json

# Sample news data structure
news_data = {
    "headline": "ක්‍රිකට් තරගයක්",
    "content": "ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම...",
    "timestamp": "2025-06-24T14:30:00",
    "url": "https://example.com/news",
    "source": "News Source",
    "category": "Sports",
    "subcategory": "Cricket",
    "persons": ["ක්‍රීඩකයා"],
    "locations": ["ශ්‍රී ලංකාව"],
    "events": ["ක්‍රිකට් තරගය"],
    "organizations": ["ක්‍රිකට් කණ්ඩායම"]
}

populate_article_from_json(news_data, manager)
manager.save()
```

3. **Run Sample Population**:

```bash
python -m scripts.populate_sample
```

## 📊 Data Structure

### News Categories Hierarchy

```
NewsCategory
├── PoliticsAndGovernance
│   ├── InternationalPolitics
│   └── DomesticPolitics
├── ScienceAndTechnology
│   ├── TechAndInnovation
│   └── ResearchAndSpace
├── CultureAndEntertainment
│   ├── ScreenAndStage
│   └── MusicAndArts
├── Sports
│   ├── Cricket
│   ├── Football
│   └── Other
└── CrimeAndJustice
    ├── CrimeReport
    └── CourtsAndInvestigation
```

### Named Entities

```
NamedEntity
├── Person (පුද්ගලයින්)
├── Organization (සංවිධාන)
├── Location (ස්ථාන)
└── Event (සිදුවීම්)
```

## 🔍 Key Features

### 1. **Multilingual Support**

- Handles Sinhala Unicode text properly
- Safe name generation for ontology identifiers
- Preserves original Sinhala content while creating machine-readable identifiers

### 2. **Contextual Relationships**

- Category-specific entity relationships (e.g., Cricket players vs Political figures)
- Temporal information with publication dates
- Source attribution and URL tracking

### 3. **Extensible Design**

- Easy to add new categories and subcategories
- Flexible entity relationship definitions
- Modular architecture for easy maintenance

### 4. **Standards Compliance**

- Uses OWL (Web Ontology Language) standard
- Compatible with semantic web tools
- Supports SPARQL queries for data retrieval

## 🔗 Semantic Relationships Architecture

The ontology system implements a sophisticated multi-layered relationship model that captures the complex semantic connections between news articles, entities, and contextual information.

### 1. **Relationship Types**

#### **Data Properties** (Literal Values)

- `hasTitle` → Article headline (string)
- `hasFullText` → Complete article content (string)
- `hasPublicationDate` → Publication timestamp (datetime)
- `hasSourceURL` → Source article URL (string)
- `canonicalName` → Primary entity name (string)
- `alias` → Alternative entity names (string array)

#### **Object Properties** (Entity-to-Entity Links)

- `hasCategory` → Links articles to news categories
- `mentionsEntity` → Generic entity mentions in articles
- `containsStatement` → Structured statement extraction
- `hasSubject` → Subject of statements/claims

### 2. **Hierarchical Category Relationships**

```python
# Category inheritance creates automatic semantic links
NewsCategory
  ├── PoliticsAndGovernance
  │   ├── InternationalPolitics  # inherits political context
  │   └── DomesticPolitics       # inherits political context
  └── Sports
      ├── Cricket               # inherits sports context
      └── Football             # inherits sports context
```

### 3. **Context-Aware Entity Relationships**

The system creates **domain-specific relationships** that provide semantic context:

#### **Political Context**

```python
# International Politics
article.hasForeignOrganization.append(organization)
article.hasForeignPerson.append(person)
article.hasForeignEvent.append(event)
article.hasForeignLocation.append(location)

# Domestic Politics
article.hasDomesticOrganization.append(organization)
article.hasDomesticPerson.append(person)
article.hasDomesticEvent.append(event)
article.hasDomesticLocation.append(location)
```

#### **Sports Context**

```python
# Cricket-specific relationships
article.hasCricketTeam.append(organization)
article.hasCricketPlayer.append(person)
article.hasCricketVenue.append(location)
article.hasCricketTournament.append(event)

# Football-specific relationships
article.hasFootballTeam.append(organization)
article.hasFootballPlayer.append(person)
article.hasFootballVenue.append(location)
article.hasFootballTournament.append(event)
```

#### **Technology Context**

```python
# Tech & Innovation
article.hasTechCompany.append(organization)
article.hasTechPerson.append(person)
article.hasTechEvent.append(event)

# Research & Space
article.hasResearchInstitution.append(organization)
article.hasResearchPerson.append(person)
article.hasResearchEvent.append(event)
```

### 4. **Relationship Creation Process**

#### **Step 1: Generic Entity Linking**

```python
# All entities are first linked generically
for entity in all_entities:
    article.mentionsEntity.append(entity)
```

#### **Step 2: Category Classification**

```python
# Article gets categorized
article.hasCategory.append(main_category)
article.hasCategory.append(sub_category)
```

#### **Step 3: Context-Specific Relationships**

```python
# Based on category, create specialized relationships

# Politics & Governance
if category == "PoliticsAndGovernance":
    if subcategory == "InternationalPolitics":
        for org in organizations:
            article.hasForeignOrganization.append(org)
        for event in events:
            article.hasForeignEvent.append(event)
        for person in persons:
            article.hasForeignPerson.append(person)
        for location in locations:
            article.hasForeignLocation.append(location)
    elif subcategory == "DomesticPolitics":
        for org in organizations:
            article.hasDomesticOrganization.append(org)
        for event in events:
            article.hasDomesticEvent.append(event)
        for person in persons:
            article.hasDomesticPerson.append(person)
        for location in locations:
            article.hasDomesticLocation.append(location)

# Science & Technology
elif category == "ScienceAndTechnology":
    if subcategory == "TechAndInnovation":
        for org in organizations:
            article.hasTechCompany.append(org)
        for event in events:
            article.hasTechEvent.append(event)
        for person in persons:
            article.hasTechPerson.append(person)
        for location in locations:
            article.hasTechLocation.append(location)
    elif subcategory == "ResearchAndSpace":
        for org in organizations:
            article.hasResearchInstitution.append(org)
        for person in persons:
            article.hasResearchPerson.append(person)
        for event in events:
            article.hasResearchEvent.append(event)
        for location in locations:
            article.hasResearchLocation.append(location)

# Culture & Entertainment
elif category == "CultureAndEntertainment":
    if subcategory == "ScreenAndStage":
        for person in persons:
            article.hasFilmDirectorActor.append(person)
        for org in organizations:
            article.hasFilmProductionCompany.append(org)
        for event in events:
            article.hasStageEvent.append(event)
        for location in locations:
            article.hasFilmLocation.append(location)
    elif subcategory == "MusicAndArts":
        for person in persons:
            article.hasMusicArtist.append(person)
        for org in organizations:
            article.hasMusicCompany.append(org)
        for event in events:
            article.hasMusicEvent.append(event)
        for location in locations:
            article.hasMusicLocation.append(location)

# Sports
elif category == "Sports":
    if subcategory == "Cricket":
        for org in organizations:
            article.hasCricketTeam.append(org)
        for person in persons:
            article.hasCricketPlayer.append(person)
        for location in locations:
            article.hasCricketVenue.append(location)
        for event in events:
            article.hasCricketTournament.append(event)
    elif subcategory == "Football":
        for org in organizations:
            article.hasFootballTeam.append(org)
        for person in persons:
            article.hasFootballPlayer.append(person)
        for location in locations:
            article.hasFootballVenue.append(location)
        for event in events:
            article.hasFootballTournament.append(event)
    elif subcategory == "Other":
        for org in organizations:
            article.hasTeam.append(org)
        for person in persons:
            article.hasPlayer.append(person)
        for location in locations:
            article.hasVenue.append(location)
        for event in events:
            article.hasTournament.append(event)

# Crime & Justice
elif category == "CrimeAndJustice":
    # Common relationships for all crime subcategories
    for person in persons:
        article.hasWitness.append(person)
    for org in organizations:
        article.hasInvestigation.append(org)

    # Subcategory-specific relationships
    if subcategory == "CrimeReport":
        for event in events:
            article.hasCrimeType.append(event)
        for location in locations:
            article.hasCrimeLocation.append(location)
    elif subcategory == "CourtsAndInvestigation":
        for event in events:
            article.hasCourtCase.append(event)
        for location in locations:
            article.hasCourtLocation.append(location)
```

### 5. **Semantic Reasoning Capabilities**

#### **Inheritance-Based Inference**

- Cricket players are automatically Sports persons
- Political events can be either International or Domestic
- Research institutions are specialized Organizations

#### **Cross-Category Analysis**

```python
# Query: Find all politicians mentioned in technology news
SPARQL: """
SELECT ?person WHERE {
    ?article hasCategory TechAndInnovation .
    ?article hasTechPerson ?person .
    ?person rdf:type Person .
}
"""
```

#### **Temporal Relationship Tracking**

```python
# Track entity mentions over time
article.hasPublicationDate = timestamp
article.mentionsEntity.append(entity)
# Enables: "When was this person first mentioned in cricket news?"
```

### 6. **Relationship Validation & Constraints**

#### **Range Restrictions**

```python
class hasCricketPlayer(ObjectProperty):
    range = [Person]  # Only Person entities allowed

class hasPublicationDate(DataProperty, FunctionalProperty):
    range = [datetime]  # Only one date per article
```

## 🔍 News Verification & Fact-Checking Process

The system implements a sophisticated multi-layered verification process that leverages the semantic relationships in the ontology to assess the credibility and accuracy of Sinhala news articles, particularly for rumor verification.

### 1. **Verification Architecture Overview**

When a Sinhala rumor/news needs verification, the system uses three complementary scoring mechanisms:

```python
# Composite verification score calculation
final_score = (
    0.4 * entity_similarity_score +      # Entity-based verification
    0.3 * semantic_similarity_score +    # Content-based verification
    0.3 * source_credibility_score       # Publisher credibility
)
```

### 2. **Entity Similarity Verification**

#### **Process Flow**

```python
# Step 1: Extract entities from input news
input_entities = {
    "persons": ["නමල් රාජපක්ෂ", "මහින්ද රාජපක්ෂ"],
    "locations": ["කොළඹ", "ශ්‍රී ලංකාව"],
    "events": ["මැතිවරණය", "රැස්වීම"],
    "organizations": ["ශ්‍රී ලංකා පොදුජන පෙරමුණ"]
}

# Step 2: Query ontology for verified entities in same context
verified_entities = query_ontology_by_category_and_subcategory(
    category="PoliticsAndGovernance",
    subcategory="DomesticPolitics"
)

# Step 3: Calculate similarity scores using fuzzy matching
entity_scores = calculate_fuzzy_similarity(input_entities, verified_entities)
```

#### **Category-Specific SPARQL Queries**

```sparql
# Example: Verify cricket players mentioned in sports news
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>
SELECT ?personName WHERE {
  ?article ns:hasCategory ?category
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketPlayer ?player.
  ?player ns:canonicalName ?personName
}

# Example: Verify political figures in domestic politics
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>
SELECT ?personName WHERE {
  ?article ns:hasCategory ?category
  FILTER (?category = ns:DomesticPolitics)
  ?article ns:hasDomesticPerson ?person.
  ?person ns:canonicalName ?personName
}
```

### 3. **Semantic Content Verification**

#### **Content Similarity Analysis**

```python
# Extract all trusted content from ontology
trusted_texts = get_all_trusted_contents()

# Use semantic similarity API for deep content analysis
payload = {
    "news_text": "ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම අද බංග්ලාදේශයට එරෙහිව...",
    "trusted_texts": [
        "ශ්‍රී ලංකාව ක්‍රිකට් තරගයක් ජයගත්තා...",
        "බංග්ලාදේශ සහ ශ්‍රී ලංකා අතර තරගය...",
        # ... more trusted content
    ]
}

semantic_score = semantic_similarity_api(payload)
```

### 4. **Source Credibility Assessment**

#### **Publisher Verification**

```python
# Get all trusted publishers from ontology
trusted_publishers = [
    "NewsFirst Sri Lanka",
    "Hiru News",
    "Ada Derana",
    # ... verified publishers
]

# Binary credibility scoring
def get_source_credibility(news_publisher, trusted_publishers):
    return 1.0 if news_publisher in trusted_publishers else 0.0
```

### 5. **Complete Verification Workflow**

#### **Input: Suspicious Sinhala News**

```python
suspicious_news = {
    "headline": "විරාත් කෝලි ශ්‍රී ලංකා කණ්ඩායමට සම්බන්ධ වෙයි",
    "content": "ඉන්දීය ක්‍රිකට් නායක විරාත් කෝලි ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායමට...",
    "source": "Unknown Blog",
    "category": "Sports",
    "subcategory": "Cricket",
    "persons": ["විරාත් කෝලි"],
    "organizations": ["ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම", "ඉන්දීය ක්‍රිකට් කණ්ඩායම"],
    "locations": ["ශ්‍රී ලංකාව", "ඉන්දියාව"],
    "events": ["ක්‍රිකට් කණ්ඩායමට සම්බන්ධ වීම"]
}
```

#### **Verification Process**

```python
# Step 1: Entity Verification
cricket_players = query_verified_cricket_players()
entity_score = fuzzy_match(["විරාත් කෝලි"], cricket_players)
# Result: High score if Virat Kohli is known cricket player

cricket_teams = query_verified_cricket_teams()
team_score = fuzzy_match(["ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම"], cricket_teams)
# Result: High score for verified team

# Step 2: Content Verification
similar_content = find_similar_cricket_news(suspicious_news.content)
content_score = semantic_similarity(suspicious_news.content, similar_content)
# Result: Low score if claim is unprecedented

# Step 3: Source Verification
source_score = verify_publisher("Unknown Blog", trusted_publishers)
# Result: 0.0 for unverified source

# Final Composite Score
final_score = 0.4 * entity_score + 0.3 * content_score + 0.3 * source_score
verification_result = "FAKE" if final_score < 0.7 else "VERIFIED"
```

### 6. **Context-Aware Verification**

#### **Category-Specific Validation**

```python
# Different verification strategies per category
if category == "PoliticsAndGovernance":
    # Check political figure consistency
    # Verify government positions
    # Cross-reference with official sources

elif category == "Sports":
    # Verify player-team relationships
    # Check tournament schedules
    # Validate venue information

elif category == "CrimeAndJustice":
    # Verify legal proceedings
    # Check court case details
    # Validate witness information
```

### 7. **Real-World Verification Examples**

#### **Example 1: Political Rumor**

```python
rumor = {
    "headline": "අගමැති ඉල්ලා අස්වෙයි",
    "persons": ["හරිනි අමරසූරිය"],
    "category": "PoliticsAndGovernance",
    "subcategory": "DomesticPolitics"
}

# Verification checks:
# ✓ Is Harini Amarasuriya a verified political figure?
# ✓ Are there similar claims in trusted sources?
# ✓ Is the source credible?
```

#### **Example 2: Sports Misinformation**

```python
rumor = {
    "headline": "ශ්‍රී ලංකාව ලෝක කුසලානය ජයගත්තා",
    "organizations": ["ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම"],
    "events": ["ලෝක කුසලානය"],
    "category": "Sports",
    "subcategory": "Cricket"
}

# Verification checks:
# ✓ Recent tournament results in ontology
# ✓ Team performance history
# ✓ Official tournament records
```

### 8. **Verification Output Format**

```python
verification_result = {
    "final_score": 0.65,
    "verdict": "SUSPICIOUS",
    "confidence": "MEDIUM",
    "breakdown": {
        "entity_similarity": 0.85,    # Entities are known
        "semantic_similarity": 0.25,  # Content is unusual
        "source_credibility": 0.0     # Unknown source
    },
    "warnings": [
        "Content significantly differs from known facts",
        "Source not in trusted publisher list",
        "Claims not corroborated by verified sources"
    ],
    "recommendations": [
        "Cross-reference with official sources",
        "Check for similar claims in trusted media",
        "Verify through primary sources"
    ]
}
```

### 9. **Integration with Real-Time Verification**

#### **API-Based Verification Service**

```python
def verify_sinhala_news(news_json):
    # Load ontology
    ontology = load_sinhala_news_ontology()

    # Extract and classify entities
    entities = extract_entities(news_json)
    category = classify_news(news_json)

    # Context-aware verification
    verification_score = multi_layer_verification(
        entities, category, news_json, ontology
    )

    return {
        "is_fake": verification_score < 0.7,
        "confidence": verification_score,
        "details": get_verification_breakdown()
    }
```

### 10. **Benefits for Sinhala Fact-Checking**

#### **Automated Detection**

- **Real-time verification** of viral Sinhala news
- **Bulk processing** of social media content
- **Early warning** for misinformation campaigns

#### **Contextual Understanding**

- **Domain-specific validation** (politics vs sports vs crime)
- **Cultural context** preservation in Sinhala language
- **Entity relationship** consistency checking

#### **Scalable Solution**

- **Growing knowledge base** through continuous learning
- **Multi-source verification** across trusted publishers
- **Semantic understanding** beyond keyword matching

This comprehensive verification system enables automated fact-checking of Sinhala news by leveraging the rich semantic relationships stored in the ontology, providing reliable rumor detection and verification capabilities.

## 🏷️ Automated News Classification System

The system employs a sophisticated machine learning-based classification pipeline specifically trained for Sinhala news content to automatically categorize articles into the appropriate ontology classes.

### 1. **Classification Architecture Overview**

The classification system uses a **hierarchical two-level approach**:

```python
# Level 1: Main Category Classification
main_categories = [
    "PoliticsAndGovernance",
    "ScienceAndTechnology",
    "CultureAndEntertainment",
    "Sports",
    "CrimeAndJustice"
]

# Level 2: Subcategory Classification
subcategory_mapping = {
    "InternationalPolitics": "PoliticsAndGovernance",
    "DomesticPolitics": "PoliticsAndGovernance",
    "TechAndInnovation": "ScienceAndTechnology",
    "ResearchAndSpace": "ScienceAndTechnology",
    "ScreenAndStage": "CultureAndEntertainment",
    "MusicAndArts": "CultureAndEntertainment",
    "Cricket": "Sports",
    "Football": "Sports",
    "Other": "Sports",
    "CrimeReport": "CrimeAndJustice",
    "CourtsAndInvestigation": "CrimeAndJustice"
}
```

### 2. **Model Architecture & Technology Stack**

#### **Transformer-Based Classification**

```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TextClassificationPipeline
)

# Load pre-trained model for Sinhala text classification
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Create classification pipeline
classifier = TextClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    return_all_scores=False,
    device=0  # GPU acceleration
)
```

#### **Label Encoding System**

```python
# Convert model predictions to human-readable categories
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Decode numeric predictions to category names
if result['label'].startswith("LABEL_"):
    sub_idx = int(result['label'].replace("LABEL_", ""))
    subcategory = label_encoder.inverse_transform([sub_idx])[0]
```

### 3. **Classification Process Flow**

#### **Step-by-Step Classification**

```python
def classify_sinhala_news(news_text):
    # Step 1: Preprocess Sinhala text
    cleaned_text = preprocess_sinhala_text(news_text)

    # Step 2: Tokenize using transformer tokenizer
    tokens = tokenizer(cleaned_text,
                      truncation=True,
                      padding=True,
                      max_length=512)

    # Step 3: Generate predictions
    result = classifier(cleaned_text)

    # Step 4: Decode labels
    subcategory = decode_prediction(result)
    main_category = subcategory_to_main[subcategory]

    # Step 5: Return structured classification
    return {
        "main_category": main_category,
        "subcategory": subcategory,
        "confidence": result['score']
    }
```

### 4. **Real-World Classification Examples**

#### **Example 1: Political News Classification**

```python
# Input Sinhala text
news_text = "ඊශ්‍රායලයෙන් ඉරානයේ ප්‍රදේශ කිහිපයකට ගුවන් ප්‍රහාර"

# Classification process
result = classifier(news_text)
# Output: {"label": "LABEL_0", "score": 0.95}

# Decode to readable format
subcategory = label_encoder.inverse_transform([0])[0]
# Result: "InternationalPolitics"

main_category = subcategory_to_main["InternationalPolitics"]
# Result: "PoliticsAndGovernance"

# Final classification
classification = {
    "main_category": "PoliticsAndGovernance",
    "subcategory": "InternationalPolitics",
    "confidence": 0.95,
    "reasoning": "Contains international conflict keywords"
}
```

#### **Example 2: Sports News Classification**

```python
# Input Sinhala text
news_text = "ශ්‍රී ලංකා ක්‍රිකට් කණ්ඩායම අද බංග්ලාදේශයට එරෙහිව තරගයට"

# Classification result
classification = {
    "main_category": "Sports",
    "subcategory": "Cricket",
    "confidence": 0.92,
    "reasoning": "Contains cricket team and match keywords"
}
```

#### **Example 3: Technology News Classification**

```python
# Input Sinhala text
news_text = "අලුත් ස්මාර්ට්ෆෝන් තාක්ෂණය නිකුත් කරයි"

# Classification result
classification = {
    "main_category": "ScienceAndTechnology",
    "subcategory": "TechAndInnovation",
    "confidence": 0.88,
    "reasoning": "Contains technology and innovation keywords"
}
```

### 5. **Integration with Ontology Population**

#### **Automated Pipeline Integration**

```python
def process_news_article(raw_news_data):
    # Step 1: Extract text content
    text_content = raw_news_data['headline'] + " " + raw_news_data['content']

    # Step 2: Automatic classification
    classification = classify_sinhala_news(text_content)

    # Step 3: Add classification to news data
    enriched_news_data = {
        **raw_news_data,
        "category": classification['main_category'],
        "subcategory": classification['subcategory'],
        "classification_confidence": classification['confidence']
    }

    # Step 4: Populate ontology with classified data
    populate_article_from_json(enriched_news_data, ontology_manager)

    return enriched_news_data
```

### 6. **Classification Quality & Accuracy**

#### **Model Performance Metrics**

```python
classification_metrics = {
    "overall_accuracy": 0.91,
    "per_category_performance": {
        "PoliticsAndGovernance": {
            "precision": 0.93,
            "recall": 0.89,
            "f1_score": 0.91
        },
        "Sports": {
            "precision": 0.95,
            "recall": 0.94,
            "f1_score": 0.94
        },
        "ScienceAndTechnology": {
            "precision": 0.87,
            "recall": 0.85,
            "f1_score": 0.86
        },
        "CultureAndEntertainment": {
            "precision": 0.89,
            "recall": 0.88,
            "f1_score": 0.88
        },
        "CrimeAndJustice": {
            "precision": 0.92,
            "recall": 0.90,
            "f1_score": 0.91
        }
    }
}
```

### 7. **Handling Classification Edge Cases**

#### **Multi-Category Content**

```python
# News that spans multiple categories
mixed_content = "අගමැති ක්‍රිකට් කණ්ඩායමේ ජයග්‍රහණය සමරයි"

# Classification strategy
def handle_mixed_content(text):
    # Primary classification
    primary = classify_sinhala_news(text)

    # Secondary classification with threshold
    if primary['confidence'] < 0.8:
        # Flag for manual review or multi-label classification
        return {
            **primary,
            "needs_review": True,
            "potential_categories": get_top_k_predictions(text, k=3)
        }

    return primary
```

#### **Low-Confidence Classifications**

```python
def validate_classification(classification_result):
    confidence_threshold = 0.7

    if classification_result['confidence'] < confidence_threshold:
        return {
            **classification_result,
            "status": "REQUIRES_MANUAL_REVIEW",
            "suggestions": [
                "Consider alternative categories",
                "Check for domain-specific terminology",
                "Verify with subject matter experts"
            ]
        }

    return {
        **classification_result,
        "status": "AUTO_CLASSIFIED"
    }
```

### 8. **Training Data & Model Fine-tuning**

#### **Training Dataset Structure**

```python
training_examples = [
    {
        "text": "ජනාධිපතිගේ නිල නිවසේ රැස්වීම",
        "category": "PoliticsAndGovernance",
        "subcategory": "DomesticPolitics"
    },
    {
        "text": "ICC ලෝක කුසලාන ක්‍රිකට් තරගාවලිය",
        "category": "Sports",
        "subcategory": "Cricket"
    },
    {
        "text": "නව AI තාක්ෂණය සමාගම විසින් දියත් කරයි",
        "category": "ScienceAndTechnology",
        "subcategory": "TechAndInnovation"
    }
    # ... thousands more examples
]
```

#### **Model Training Process**

```python
# Fine-tuning pipeline for Sinhala news classification
def train_classification_model():
    # 1. Load pre-trained transformer model
    base_model = "bert-base-multilingual-cased"

    # 2. Prepare Sinhala news dataset
    train_dataset = load_sinhala_news_dataset()

    # 3. Fine-tune on domain-specific data
    trainer = train_transformer_classifier(
        model=base_model,
        train_data=train_dataset,
        validation_data=validation_dataset,
        num_epochs=10,
        learning_rate=2e-5
    )

    # 4. Save trained model
    trainer.save_model("./sinhala_news_classifier")
```
