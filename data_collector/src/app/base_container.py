from src.services.config_service import ConfigService
from src.services.data_service import DataService

from src.utils.singleton import Singleton

from dataclasses import dataclass

@dataclass
class BaseContainer(metaclass=Singleton):
    config_service: ConfigService
    data_service: DataService
