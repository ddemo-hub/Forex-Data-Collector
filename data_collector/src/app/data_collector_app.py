from src.services.config_service import ConfigService

from src.utils.singleton import Singleton

from collectors import *

from apscheduler.schedulers.background import BackgroundScheduler

class DataCollectorApp(metaclass=Singleton):
    def __init__(
        self, 
        config_service: ConfigService, 
        tcmb_collector: TCMBCollector,
        yapikredi_collector: YapiKrediCollector,
        ziraat_collector: ZiraatCollector,
        altinkaynak_collector: AltinkaynakCollector,
        kapalicarsi_collector: KapaliCarsiCollector
    ):
        self.config_service = config_service
        self.tcmb_collector = tcmb_collector
        self.yapikredi_collector = yapikredi_collector
        self.ziraat_collector = ziraat_collector
        self.altinkaynak_collector = altinkaynak_collector
        self.kapalicarsi_collector = kapalicarsi_collector

    def schedule_jobs(self, scheduler: BackgroundScheduler):
        tcmb_cron = self.config_service.tcmb_cron
        scheduler.add_job(
            TCMBCollector.run,
            args=[self.tcmb_collector],
            trigger="cron", 
            day_of_week=tcmb_cron["day_of_week"], hour=tcmb_cron["hour"], minute=tcmb_cron["minute"]
        )
        
        scheduler.add_job(
            YapiKrediCollector.run,
            args=[self.yapikredi_collector],
            trigger="cron", 
            second=self.config_service.yapikredi_cron["second"]
        )
        
        scheduler.add_job(
            ZiraatCollector.run,
            args=[self.ziraat_collector],
            trigger="cron", 
            second=self.config_service.ziraat_cron["second"]
        )
    
        scheduler.add_job(
            AltinkaynakCollector.run,
            args=[self.altinkaynak_collector],
            trigger="cron", 
            second=self.config_service.altinkaynak_cron["second"]
        )
    
        scheduler.add_job(
            KapaliCarsiCollector.run,
            args=[self.kapalicarsi_collector],
            trigger="cron", 
            second=self.config_service.kapalicarsi_cron["second"]
        )
        ...
                
        return scheduler
    
    def run_all(self):
        #TODO THE COLLECTORS SHOULD RUN CONCURRENTLY IN DIFFERENT THREADS
        
        self.tcmb_collector.run()
        self.yapikredi_collector.run()
        self.ziraat_collector.run()
        self.altinkaynak_collector.run()
        self.kapalicarsi_collector.run()
        
        ...