from .base_controller import BaseController

from flask_socketio import Namespace

class WebsocketEvents(Namespace, BaseController):
    def __init__(self, namespace: str, base_container):
        super(Namespace, self).__init__(namespace)
        super(BaseController, self).__init__(base_container)
        
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass
    
    def example_event(self, *args):
        ...

    ...