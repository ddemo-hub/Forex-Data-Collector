from src.app.base_container import BaseContainer

class BaseController():
    def __init__(self, base_container: BaseContainer):
        self.config_service = base_container.config_service
        self.data_service = base_container.data_service