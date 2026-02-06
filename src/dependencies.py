from functools import lru_cache
from typing import Annotated, Generator

from fastapi import Depends, Request

from sqlalchemy.orm import Session
from src.config import Settings
from src.db.interfaces.base import BaseDatabase

@lru_cache
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


def get_request_settings(request: Request) -> Settings:
    """Get settings from the request state."""
    return request.app.state.settings


def get_database(request: Request) -> BaseDatabase:
    """Get database from the request state."""
    return request.app.state.database


def get_db_session(database: Annotated[BaseDatabase, Depends(get_database)]) -> Generator[Session, None, None]:
    """Get database session dependency."""
    with database.get_session() as session:
        yield session


# def get_pdf_parser_service(request: Request):
#     """Get PDF parser service from app state (Week 2+ - not implemented yet)."""
#     return None


# def get_opensearch_service(request: Request):
#     """Get OpenSearch service from app state (Week 3+ - placeholder for Week 1)."""
#     return getattr(request.app.state, "opensearch_service", None)


# def get_llm_service(request: Request):
#     """Get LLM service from app state (Phase 3 - not implemented yet)."""
#     return None


# Dependency type aliases for better type hints
SettingsDep = Annotated[Settings, Depends(get_settings)]
DatabaseDep = Annotated[BaseDatabase, Depends(get_database)]
SessionDep = Annotated[Session, Depends(get_db_session)]
# PDFParserServiceDep = Annotated[object, Depends(get_pdf_parser_service)]
# OpenSearchServiceDep = Annotated[object, Depends(get_opensearch_service)]
# LLMServiceDep = Annotated[object, Depends(get_llm_service)]