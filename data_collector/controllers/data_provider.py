from src.services.config_service import ConfigService
from src.services.data_service import DataService

from src.utils.globals import Globals

from flask.views import MethodView
from flask import request

class DataProvider(MethodView):
    init_every_request= False
    
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service

        
    def get(self):
        pass
