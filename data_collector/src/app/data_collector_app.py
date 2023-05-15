from src.services.config_service import ConfigService
from src.services.data_service import DataService 

from src.utils.singleton import Singleton

from collectors import *

from apscheduler.schedulers.background import BackgroundScheduler

class DataCollectorApp(metaclass=Singleton):
    def __init__(
        self, 
        config_service: ConfigService, 
        data_service: DataService,
    ):
        self.config_service = config_service
        self.data_service = data_service
        
        ...

    def schedule_jobs(self, scheduler: BackgroundScheduler):
        pass