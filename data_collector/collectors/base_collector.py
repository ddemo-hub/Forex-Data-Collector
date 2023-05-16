from src.utils.singleton import Singleton
from src.utils.globals import Globals
from src.utils.logger import Logger

from src.app.base_container import BaseContainer

class BaseCollector(metaclass=Singleton):
    def __init__(self, base_container: BaseContainer):
        self.config_service = base_container.config_service
        self.data_service = base_container.data_service
        
        self.logger = Logger
        self.hooks = Globals.hooks