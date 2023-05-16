from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from controllers.service_controller import ServiceController

from src.app.app_container import AppContainer 

from src.utils.globals import Globals
from src.utils.logger import Logger

Logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))


def create_scheduler(app_container: AppContainer):
    scheduler = BackgroundScheduler(daemon=True)
    
    ...
    
    return scheduler

def create_app(app_container: AppContainer):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key
    
    app.add_url_rule(
        "/data_collector", 
        view_func=ServiceController.as_view(
            "data_collector", 
            config_service=app_container.config_service, 
            data_service=app_container.data_service
        )
    )
    
    return app

if __name__ == "__main__":
    scheduler = create_scheduler(AppContainer)
    app = create_app(AppContainer)
    
    scheduler.start()
    app.run()
