from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging

# Import ontology modules
from modules.similarity_matching.similarity_engine import get_semantic_similarity_score
from modules.similarity_matching.checker import check_news
from modules.pre_processing.news_classification import get_category_subcategory
from modules.pre_processing.news_detection import get_news_or_not
from modules.pre_processing.ner import extract_named_entities
from modules.pre_processing import sinhala_preprocessor
from modules.simulations.simulations import simulate_news_verification
from modules.dynamic_ontology.manager import OntologyManager
from modules.dynamic_ontology.models import (
    NewsArticleCreate,
    NewsArticleResponse,
    BulkPopulateRequest,
    BulkPopulateResponse,
)
from modules.dynamic_ontology.populator import (
    populate_article_from_json,
    populate_bulk_articles,
)


class VerifyNewsRequest(BaseModel):
    """Request model for verifying news articles"""

    text: str


class SimilarityCheckRequest(BaseModel):
    """Request model for checking similarity of news content"""

    news_text: str
    trusted_text: str


class CheckNewsModel(BaseModel):
    """Model for checking news articles"""

    content: str
    category: str
    subcategory: str
    persons: list[str] = []
    locations: list[str] = []
    events: list[str] = []
    organizations: list[str] = []


class NewsArticleFromSource(BaseModel):
    """Model for news article from source"""

    headline: str
    content: str
    source: str
    timestamp: str
    url: str


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="News Verifier Backend API",
    description="Backend API for News Verification System with Dynamic Ontology Management",
    version="1.0.0",
    root_path="/api",
)

# Global ontology manager instance
ontology_manager = None


@app.on_event("startup")
async def startup_event():
    """Initialize the ontology manager on startup"""
    global ontology_manager, sinhala_preprocessor
    try:
        logger.info("Initializing ontology manager...")
        ontology_manager = OntologyManager()

        logger.info("Ontology manager initialized successfully")

        logger.info("Initializing Sinhala preprocessor...")
        sinhala_preprocessor = sinhala_preprocessor.SinhalaPreprocessor()

        logger.info("Sinhala preprocessor initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ontology manager: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "News Verifier Backend API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        stats = ontology_manager.get_ontology_stats() if ontology_manager else {}
        return {
            "status": "healthy",
            "ontology_loaded": ontology_manager is not None,
            "ontology_stats": stats,
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "error": str(e)},
        )


@app.get("/ontology/stats", tags=["Ontology"])
async def get_ontology_stats():
    """Get ontology statistics"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    try:
        stats = ontology_manager.get_ontology_stats()
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Error getting ontology stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error getting ontology stats: {str(e)}"
        )


@app.post(
    "/ontology/populate-article", response_model=NewsArticleResponse, tags=["Ontology"]
)
async def populate_single_article(article: NewsArticleCreate):
    """Populate a single news article into the ontology"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    try:
        # Convert Pydantic model to dict
        article_data = article.dict()

        # Populate the article
        article_individual = populate_article_from_json(article_data, ontology_manager)

        # Save the ontology
        ontology_manager.save()

        logger.info(f"Successfully populated article: {article.headline}")

        return NewsArticleResponse(
            success=True,
            message="Article populated successfully",
            article_id=str(article_individual.name)
            if hasattr(article_individual, "name")
            else None,
        )

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error populating article: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error populating article: {str(e)}"
        )


@app.post(
    "/ontology/populate-bulk", response_model=BulkPopulateResponse, tags=["Ontology"]
)
async def populate_bulk_articles_endpoint(request: BulkPopulateRequest):
    """Populate multiple news articles into the ontology"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    if not request.data:
        raise HTTPException(status_code=400, detail="No articles provided")

    try:
        # Convert Pydantic models to dicts
        articles_data = [article.dict() for article in request.data]

        logger.info(f"Starting bulk population of {len(articles_data)} articles")

        # Populate articles
        results = populate_bulk_articles(articles_data, ontology_manager)

        logger.info(
            f"Bulk population completed. Success: {results['successful']}, Failed: {results['failed']}"
        )

        return BulkPopulateResponse(
            success=results["failed"] == 0,  # Success only if no failures
            message=f"Processed {results['total_processed']} articles. "
            f"Successful: {results['successful']}, Failed: {results['failed']}",
            total_processed=results["total_processed"],
            successful=results["successful"],
            failed=results["failed"],
            errors=results["errors"],
        )

    except Exception as e:
        logger.error(f"Error in bulk population: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error in bulk population: {str(e)}"
        )


@app.post("/ontology/preprocess-n-populate", tags=["Ontology"])
async def preprocess_and_populate(request: NewsArticleFromSource):
    """Endpoint to preprocess text and populate into ontology"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    try:
        # Preprocess the text
        preprocessed_text = sinhala_preprocessor.preprocess_text(request.content)

        # Get category and subcategory
        category, subcategory = get_category_subcategory(preprocessed_text)

        if not category or not subcategory:
            raise HTTPException(
                status_code=400,
                detail="Could not determine category or subcategory from the content.",
            )

        # Extract named entities
        persons, locations, events, organizations = extract_named_entities(
            preprocessed_text
        )

        # Create a NewsArticleCreate instance
        article_data = NewsArticleCreate(
            headline=request.headline,
            content=preprocessed_text,
            source=request.source,
            timestamp=request.timestamp,
            url=request.url,
            category=category,
            subcategory=subcategory,
            persons=persons,
            locations=locations,
            events=events,
            organizations=organizations,
        )

        # Populate the article into the ontology
        article_individual = populate_article_from_json(
            article_data.dict(), ontology_manager
        )

        # Save the ontology
        ontology_manager.save()

        return NewsArticleResponse(
            success=True,
            message="Article populated successfully",
            article_id=str(article_individual.name)
            if hasattr(article_individual, "name")
            else None,
        )

    except Exception as e:
        logger.error(f"Error preprocessing and populating article: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error preprocessing and populating article: {str(e)}",
        )


@app.post("/news/verify", tags=["News Verification"])
async def verify_news(request: VerifyNewsRequest):
    """Endpoint to verify a news article"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    flow = []

    try:
        # Convert Pydantic model to dict
        article_data = request.text

        # STEP 01: Pre-processing text (remove unnecessary characters, english stop words, etc.)
        article_data = sinhala_preprocessor.preprocess_text(article_data)
        flow.append({"step": "Pre-processing", "result": article_data})

        # STEP 02: Verify whether the news is a news or not.
        checked_news = get_news_or_not(article_data)
        flow.append({"step": "News Detection", "result": checked_news})
        print(f"[DEBUG] is_news: {checked_news}")

        # STEP 03: Do classification , sub-categorization, etc.
        classification_result = get_category_subcategory(article_data)
        print(f"[DEBUG] Classification result: {classification_result}")
        flow.append(
            {
                "step": "Classification",
                "result": "Category: "
                + classification_result[0]
                + ", Subcategory: "
                + classification_result[1],
            }
        )

        # Check if category and subcategory are valid
        if classification_result[0] == "" or classification_result[1] == "":
            raise HTTPException(
                status_code=400, detail="Could not determine category or subcategory."
            )

        # STEP 04: Extract named entities using NER service
        persons, locations, events, organizations = extract_named_entities(article_data)
        print(
            f"[DEBUG] Extracted entities: persons={persons}, locations={locations}, events={events}, organizations={organizations}"
        )
        flow.append(
            {
                "step": "Named Entity Recognition",
                "result": f"persons={persons}, locations={locations}, events={events}, organizations={organizations}",
            }
        )

        formatted_article_data = CheckNewsModel(
            content=article_data,
            category=classification_result[0],
            subcategory=classification_result[1],
            persons=persons,
            locations=locations,
            events=events,
            organizations=organizations,
        )

        # STEP 05: Do the similarity checking with ontology.
        result = check_news(
            news_json=formatted_article_data.dict(),
            ontology_manager=ontology_manager,
            debug=True,
        )

        result["flow"] = flow

        return result

    except Exception as e:
        logger.error(f"Error verifying news article: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error verifying news article: {str(e)}"
        )


@app.post("/news/verify/simulate", tags=["News Verification"])
async def simulate_verify_news(request: VerifyNewsRequest):
    """Simulate news verification for testing purposes"""

    flow = []

    cleaned = sinhala_preprocessor.preprocess_text(request.text)
    flow.append({"step": "Pre-processing", "result": cleaned})

    result = simulate_news_verification(cleaned)

    result["flow"] = flow
    return result


@app.post("/similarity/check", tags=["Similarity Matching"])
async def check_similarity(request: SimilarityCheckRequest):
    """Endpoint to check similarity of news content"""

    try:
        # Convert Pydantic model to dict
        news_data = request.dict()

        # Perform similarity check
        result = get_semantic_similarity_score(
            news_text=news_data["news_text"],
            trusted_texts=[news_data["trusted_text"]],
        )

        return result

    except Exception as e:
        logger.error(f"Error checking similarity: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error checking similarity: {str(e)}"
        )


@app.post("/pre-processing/preprocess", tags=["Pre-processing"])
async def preprocess_text(request: VerifyNewsRequest):
    """Endpoint to preprocess text"""

    try:
        # Call the preprocessing function
        result = sinhala_preprocessor.preprocess_text(request.text)
        return {"preprocessed_text": result}

    except Exception as e:
        logger.error(f"Error preprocessing text: {e}")
        raise HTTPException(status_code=500, detail="Error preprocessing text")


@app.post("/pre-processing/detect-news", tags=["Pre-processing"])
async def detect_news(request: VerifyNewsRequest):
    """Endpoint to detect news"""
    try:
        # Call the news detection function
        result = get_news_or_not(request.text)
        return {"is_news": result}

    except Exception as e:
        logger.error(f"Error detecting news: {e}")
        raise HTTPException(status_code=500, detail="Error detecting news")


@app.post("/pre-processing/classify", tags=["Pre-processing"])
async def classify_news(request: VerifyNewsRequest):
    """Endpoint to classify news"""
    try:
        # Call the classification function
        category, subcategory = get_category_subcategory(request.text)
        return {"category": category, "subcategory": subcategory}

    except Exception as e:
        logger.error(f"Error classifying news: {e}")
        raise HTTPException(status_code=500, detail="Error classifying news")


@app.post("/pre-processing/ner", tags=["Pre-processing"])
async def extract_entities(request: VerifyNewsRequest):
    """Endpoint to extract named entities from news text"""
    try:
        # Call the NER extraction function
        persons, locations, events, organizations = extract_named_entities(request.text)
        return {
            "persons": persons,
            "locations": locations,
            "events": events,
            "organizations": organizations,
        }

    except Exception as e:
        logger.error(f"Error extracting named entities: {e}")
        raise HTTPException(status_code=500, detail="Error extracting named entities")


if __name__ == "__main__":
    # WHEN RUNNING ON DOCKER
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

    # LOCAL DEVELOPMENT ON 127.0.0.1 (SPECIALLY ON WINDOWS)
    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
