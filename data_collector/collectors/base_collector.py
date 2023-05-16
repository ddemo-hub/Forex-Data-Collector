from src.utils.singleton import Singleton
from src.utils.logger import Logger

class BaseCollector(metaclass=Singleton):
    def __init__(self, base_collector_container):
        self.config_service = base_collector_container.config_service
        self.data_service = base_collector_container.data_service
        
        self.logger = Logger
