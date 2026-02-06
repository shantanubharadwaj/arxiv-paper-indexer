import asyncio
import logging
import time
import xml.etree.ElementTree as ET
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote, urlencode

import httpx
from src.config import ArxivSettings
from src.exceptions import ArxivAPIException, ArxivAPITimeoutError, ArxivParseError, PDFDownloadException, PDFDownloadTimeoutError
from src.schemas.arxiv.paper import ArxivPaper

logger = logging.getLogger(__name__)


class ArxivClient:
    """Client for fetching paper from arXiv API."""
    
    def __init__(self, settings: ArxivSettings):
        self._settings = settings
        self._last_request_time: Optional[float] = None
        
    @cached_property
    def pdf_cache_dir(self) -> Path:
        """PDF cache directory with lazy creation."""
        cache_dir = Path(self._settings.pdf_cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    
    @property
    def base_url(self) -> str:
        return self._settings.base_url
    
    @property
    def namespaces(self) -> dict:
        return self._settings.namespaces
    
    @property
    def rate_limit_delay(self) -> float:
        return self._settings.rate_limit_delay
    
    @property
    def timeout_seconds(self) -> int:
        return self._settings.timeout_seconds
    
    @property
    def max_results(self) -> int:
        return self._settings.timeout_seconds
    
    @property
    def search_category(self) -> str:
        return self._settings.search_category
    
    async def fetch_papers(
        self,
        max_results: Optional[int] = None,
        start: int = 0,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[ArxivPaper]:
        """
        Fetch Papers from arXiv for the configured category

        Args:
            max_results: Maximum number of papers to fetch (uses settings default if None)
            start: Starting index for pagination
            sort_by: Sort criteria (submittedDate, lastUpdatedDate, relevance)
            sort_order: Sort order (ascending, descending)
            from_date: Filter papers submitted after this date (format: YYYYMMDD)
            to_date: Filter papers submitted before this date (format: YYYYMMDD)

        Returns:
            List of ArxivPaper objects for the configured category
        """
        
        if max_results is None:
            max_results = self.max_results
            
        # Build search query
        search_query = f"cat:{self.search_category}"
        
        # Add date filtering if provided
        if from_date or to_date:
    
    