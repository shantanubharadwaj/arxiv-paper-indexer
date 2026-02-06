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

logger = logging.getLogger(__name__)

class ArxivClient:
    """Client for fetching papers from arXiv API."""
    
    def __init__(self, settings: ArxivSettings):
        self._settings = settings
        self._last_request_time: Optional[float] = None
        
    @cached_property
    def pdf_cache_dir(self) -> Path:
        """PDF cache directory with lazy creation."""
        cache_dir = Path(self._settings.pdf_ca)