from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


@dataclass(slots=True)
class FormattedNewsArticle:
    """Typed container for scraped / pre-processed news."""

    headline: str
    content: str
    timestamp: datetime
    url: str
    source: str


# Pydantic models for API validation
class NewsArticleCreate(BaseModel):
    """Model for creating news articles via API"""

    headline: str
    content: str
    timestamp: str  # Will be parsed to datetime
    url: str
    source: str
    category: str
    subcategory: str
    persons: List[str] = []
    locations: List[str] = []
    events: List[str] = []
    organizations: List[str] = []


class NewsArticleResponse(BaseModel):
    """Response model for created news articles"""

    success: bool
    message: str
    article_id: Optional[str] = None


class BulkPopulateRequest(BaseModel):
    """Model for bulk population requests"""

    data: List[NewsArticleCreate]


class BulkPopulateResponse(BaseModel):
    """Response model for bulk population"""

    success: bool
    message: str
    total_processed: int
    successful: int
    failed: int
    errors: List[str] = []
