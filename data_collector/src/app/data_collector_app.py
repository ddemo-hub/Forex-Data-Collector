from src.services.config_service import ConfigService

from src.utils.singleton import Singleton

from collectors import *

from apscheduler.schedulers.background import BackgroundScheduler

class DataCollectorApp(metaclass=Singleton):
    def __init__(
        self, 
        config_service: ConfigService, 
        tcmb_collector: TCMBCollector
    ):
        self.config_service = config_service
        self.tcmb_collector = tcmb_collector

    def schedule_jobs(self, scheduler: BackgroundScheduler):
        tcmb_cron = self.config_service.tcmb_cron
        scheduler.add_job(
            TCMBCollector.run,
            args=[self.tcmb_collector],
            trigger="cron", 
            day_of_week=tcmb_cron["day_of_week"], hour=tcmb_cron["hour"], minute=tcmb_cron["minute"]
        )

        ...
                
        return scheduler
    
    def run_all(self):
        #TODO THE COLLECTORS SHOULD RUN CONCURRENTLY IN DIFFERENT THREADS
        
        self.tcmb_collector.run()
        
        ...