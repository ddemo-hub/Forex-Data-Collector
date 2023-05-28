from src.utils.singleton import Singleton
from src.utils.globals import Globals

from src.services.config_service import ConfigService
from src.services.data_service import DataService

from .base_container import BaseContainer
from .data_collector_app import DataCollectorApp

from collectors import *

from dataclasses import dataclass

@dataclass
class AppContainer(metaclass=Singleton):
    config_service = ConfigService(
        configs=Globals.project_path.joinpath("src", "configs")
    )
    
    data_service = DataService(config_service=config_service)
    
    base_container = BaseContainer(config_service=config_service, data_service=data_service)

    tcmb_collector = TCMBCollector(base_container)
    yapikredi_collector = YapiKrediCollector(base_container)

    ...

    data_collector_app = DataCollectorApp(
        config_service=config_service, 
        tcmb_collector=tcmb_collector,
        
    )
