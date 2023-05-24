from .base_collector import BaseCollector

class YapiKrediCollector(BaseCollector):
    cron: dict
    
    def __init__(self, base_container):
        super().__init__(base_container)
        type(self).cron = self.config_service.tcmb_cron

    def run(self):
        pass