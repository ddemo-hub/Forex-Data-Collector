from src.services.config_service import ConfigService
from src.services.data_service import DataService

from src.utils.globals import Globals

from flask import request, jsonify, make_response
from flask.views import MethodView

class WebhookRegistrar(MethodView):
    init_every_request= False
    
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service

        
    def get(self):
        try:
            hook = request.json
            
            # Construct the address
            hook_address = f"{request.remote_addr}/{hook['port']}"
            
            # Construct the dictionary that holds the required data for the hook connection
            hook["address"] = hook_address
            hook.pop("port")
            
            # Update cache
            cached_hooks = Globals.cache.get("hooks")
            cached_hooks.append(hook)
            Globals.cache.set("hooks", cached_hooks)
            
            return make_response(jsonify("success"), 200)
        except Exception as ex:
            return make_response(jsonify(ex), 400)
        
