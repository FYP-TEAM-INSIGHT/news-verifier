from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import logging

# Import ontology modules
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


@app.get("/ontology/stats")
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


@app.post("/ontology/populate-article", response_model=NewsArticleResponse)
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


@app.post("/ontology/populate-bulk", response_model=BulkPopulateResponse)
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


@app.post("/news/verify")
async def verify_news(request: VerifyNewsRequest):
    """Endpoint to verify a news article"""
    if not ontology_manager:
        raise HTTPException(status_code=503, detail="Ontology manager not initialized")

    try:
        # Convert Pydantic model to dict
        article_data = request.text

        # Here you would implement the logic to verify the news article

        # STEP 01: Pre-processing text (remove unnecessary characters, english stop words, etc.)
        article_data = sinhala_preprocessor.preprocess_text(article_data)

        # STEP 02: Verify whether the news is a news or not.
        checked_news = get_news_or_not(article_data)
        print(f"[DEBUG] is_news: {checked_news}")
        if checked_news != "news":
            raise HTTPException(
                status_code=400,
                detail="The provided content is not recognized as news. It is categorized as: "
                + checked_news,
            )

        # STEP 03: Do classification , sub-categorization, etc.
        classification_result = get_category_subcategory(article_data)
        print(f"[DEBUG] Classification result: {classification_result}")
        if classification_result[0] == "" or classification_result[1] == "":
            raise HTTPException(
                status_code=400, detail="Could not determine category or subcategory."
            )

        # STEP 04: Extract named entities using NER service
        entities = extract_named_entities(article_data)
        print(entities)

        # STEP 05: Do the similarity checking with ontology.
        # result = check_news({content: article_data, category: "news", subcategory: "general"}, ontology_manager, debug=True)

        # For now, we will just return the article data as a placeholder
        return {"success": True, "article": article_data, "entities": entities}

    except Exception as e:
        logger.error(f"Error verifying news article: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error verifying news article: {str(e)}"
        )


@app.post("/news/verify/simulate")
async def simulate_verify_news(request: VerifyNewsRequest):
    """Simulate news verification for testing purposes"""

    # STEP 01: Pre-processing text (remove unnecessary characters, english stop words, etc.)
    cleaned_text = sinhala_preprocessor.preprocess_text(request.text)
    logger.info(f"cleaned_text: {cleaned_text}")

    entities = extract_named_entities(cleaned_text)
    logger.info(f"Extracted entities: {entities}")

    return simulate_news_verification(cleaned_text)


if __name__ == "__main__":
    # WHEN RUNNING ON DOCKER
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")

    # LOCAL DEVELOPMENT ON 127.0.0.1 (SPECIALLY ON WINDOWS)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")
