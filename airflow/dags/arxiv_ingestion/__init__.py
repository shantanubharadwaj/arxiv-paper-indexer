import asyncio
import logging
import sys
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Tuple

sys.path.insert(0, "/opt/airflow")

from sqlalchemy import text
from src.db.factory import make_database
