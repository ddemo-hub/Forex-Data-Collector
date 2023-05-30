import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_caching import Cache
from flask_socketio import SocketIO
 
from data_collector.controllers.webhook_registrar import WebhookRegistrar
from data_collector.controllers.websocket_events import WebsocketEvents
from data_collector.controllers.main_controller import MainController
from data_collector.controllers.data_provider import DataProvider

from src.app.app_container import AppContainer 

from src.utils.globals import Globals
from src.utils.logger import Logger

Logger.set_logger_path(Globals.artifacts_path.joinpath("logs.txt"))


def create_app(app_container: AppContainer):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = app_container.config_service.secret_key
    
    # Initialize API endpoints
    app.add_url_rule(
        "/register_webhook", 
        view_func=WebhookRegistrar.as_view(
            "webhook_registrar", 
            base_container=app_container.base_container
        )
    )
    app.add_url_rule(
        "/data_provider", 
        view_func=DataProvider.as_view(
            "data_provider", 
            base_container=app_container.base_container
        )
    )
    
    # Initialize Browser endpoints
    app.add_url_rule(
        "/", 
        view_func=MainController.as_view(
            "main", 
            base_container=app_container.base_container
        )
    )
    
    ...
        
    return app

def create_cache(app_container: AppContainer, flask_app: Flask):
    # Initialize Cache
    cache = Cache()
    cache.init_app(app=flask_app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': Globals.cache_path})
    
    # Set cache keys
    cache.set("hooks", [])
    for currency in app_container.config_service.currencies:
        dict_exchanges = {exchange: 0 for exchange in app_container.config_service.exchanges}
        cache.set(f"{currency}_BUY", dict_exchanges)
        cache.set(f"{currency}_SELL", dict_exchanges)    

    return cache

def main(app_container: AppContainer):
    # Create App
    flask_app = create_app(app_container)
    
    # Create Cache
    cache = create_cache(app_container, flask_app)
    Globals.cache = cache
    
    # Create Websocket
    socketio = SocketIO(flask_app)
    socketio.on_namespace(WebsocketEvents("/", app_container.base_container))
    Globals.socketio = socketio

    # Create Scheduler
    scheduler = BackgroundScheduler()
    scheduler = app_container.data_collector_app.schedule_jobs(scheduler=scheduler)
    
    # Run all collectors once before starting the scheduler and the app
    app_container.data_collector_app.run_all()
    
    # Start the scheduler and the Flask app
    scheduler.start()
    socketio.run(flask_app)
    

if __name__ == "__main__":
    main(AppContainer)
