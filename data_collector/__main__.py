import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_caching import Cache
from flask_socketio import SocketIO
 
from data_collector.controllers.webhook_registrar import WebhookRegistrar
from data_collector.controllers.data_provider import DataProvider
from data_collector.controllers.main_controller import MainController

from src.app.app_container import AppContainer 

from src.utils.globals import Globals
from src.utils.logger import Logger

Logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))


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
    app.add_url_rule(
        "/", 
        view_func=MainController.as_view(
            "main", 
            config_service=app_container.config_service, 
            data_service=app_container.data_service
        )
    )
    
    ...
        
    return app

def create_socketio(app_container: AppContainer, flask_app: Flask):
    socketio = SocketIO(flask_app)
    
    socketio.on_event("example event", app_container.websocket_events.example_event)
    
    ...
    
    return socketio

def main(app_container: AppContainer):
    # Create App
    flask_app = create_app(app_container)
    
    # Create Cache
    Globals.cache = Cache()
    Globals.cache.init_app(app=flask_app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Globals.cache_path})
    Globals.cache.set("hooks", [])
    
    # Create Websocket
    socketio = create_socketio(app_container, flask_app)
    Globals.socketio = socketio

    # Create Scheduler
    scheduler = BackgroundScheduler()
    scheduler = app_container.data_collector_app.schedule_jobs(scheduler=scheduler)
    
    # Start the scheduler and the Flask app
    scheduler.start()
    socketio.run(flask_app)
    

if __name__ == "__main__":
    main(AppContainer)