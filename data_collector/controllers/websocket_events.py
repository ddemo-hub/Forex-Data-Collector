from src.services.config_service import ConfigService
from src.services.data_service import DataService

class WebsocketEvents():
    config_service: ConfigService
    data_service: DataService

    def __init__(self, config_service: ConfigService, data_service: DataService):
        type(self).config_service = config_service
        type(self).data_service = data_service
        
    @staticmethod
    def example_event():
        # WebsocketEvents.config_service......
        pass
    
    ...