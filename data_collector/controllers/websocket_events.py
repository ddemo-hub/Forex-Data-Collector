from .base_controller import BaseController

from flask_socketio import Namespace

class WebsocketEvents(Namespace):
    def __init__(self, namespace: str, base_container):
        super().__init__(namespace)
        
        self.config_service = base_container.config_service
        self.data_service = base_container.data_service
        
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass
    
    def example_event(self, *args):
        ...

    ...