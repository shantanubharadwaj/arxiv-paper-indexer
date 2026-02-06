import logging
from typing import Dict

import httpx
from src.config import Settings

logger = logging.getLogger(__name__)

class OllamaClient:
    
    def __init__(self, settings: Settings):
        self.base_url = settings.ollama_host
        
    async def health_check(self) -> Dict[str, str]:
        """Check if Ollama service is available."""
        try:
            logger.info(f"1. Ollama response ")
            async with httpx.AsyncClient(timeout=5.0) as client:
                logger.info(f"2. Ollama response: {self.base_url}/api/tags >> {client}")
                response = await client.get(f"{self.base_url}/api/tags")
                logger.info(f"Ollama response : {response}")
                if response.status_code == 200:
                    return {"status": "healthy", "message": "Ollama service is running"}
                else:
                    return {"status": "unhealthy", "message": f"HTTP {response.status_code}"}
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}