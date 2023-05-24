import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_caching import Cache
 
from collectors import *
 
from data_collector.controllers.webhook_registrar import WebhookRegistrar
from data_collector.controllers.data_provider import DataProvider

from src.app.app_container import AppContainer 

from src.utils.globals import Globals
from src.utils.logger import Logger

Logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))


def create_scheduler(app_container: AppContainer):
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        TCMBCollector.run,
        args=[app_container.tcmb_collector],
        trigger="cron", 
        day_of_week=TCMBCollector.cron["day_of_week"], hour=TCMBCollector.cron["hour"], minute=TCMBCollector.cron["minute"]
    )
    
    ...
    
    return scheduler

def create_app(app_container: AppContainer):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key
    
    app.add_url_rule(
        "/register_webhook", 
        view_func=WebhookRegistrar.as_view(
            "webhook_registrar", 
            config_service=app_container.config_service, 
            data_service=app_container.data_service
        )
    )
    app.add_url_rule(
        "/data_provider", 
        view_func=DataProvider.as_view(
            "data_provider", 
            config_service=app_container.config_service, 
            data_service=app_container.data_service
        )
    )
        
    return app

if __name__ == "__main__":
    scheduler = create_scheduler(AppContainer)
    app = create_app(AppContainer)
    
    Globals.cache = Cache()
    Globals.cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Globals.cache_path})
    Globals.cache.set("hooks", [])
    
    scheduler.start()
    app.run()
