from .singleton import Singleton

from flask_caching import Cache

from dataclasses import dataclass
from datetime import datetime 
import pathlib

@dataclass
class Globals(metaclass=Singleton):
    DATETIME_NOW = datetime.now().strftime("%Y_%B/Day_%d/%H.%M.%S")
    
    # Paths
    project_path = pathlib.Path(__file__).parent.parent.parent
    
    artifacts_path = project_path.parent.joinpath("artifacts", DATETIME_NOW)
    db_schema_path = project_path.parent.joinpath("schema.sql")

    cache_path = artifacts_path.joinpath("cache")
    cache: Cache
