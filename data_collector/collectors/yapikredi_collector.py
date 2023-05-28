from src.utils.globals import Globals
from src.utils.logger import Logger

from .base_collector import BaseCollector

class YapiKrediCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__(base_container)

    def run(self):
        pass