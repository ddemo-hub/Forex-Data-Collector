from .base_controller import BaseController

from src.utils.globals import Globals
from src.utils.logger import Logger 


from flask import request, jsonify, make_response
from flask.views import MethodView

class WebhookRegistrar(MethodView, BaseController):
    init_every_request= False
    
    def __init__(self, base_container):
        super().__init__(base_container)

    def get(self):
        try:
            hook = request.json
            
            if hook.keys() >= {"port", "exchanges", "currencies"}:
                return make_response(jsonify("Missing parameters. A valid request must contain the parameters 'port', 'currencies' and 'exchanges'"), 400)
            
            # Construct the address
            hook_address = f"{request.remote_addr}:{hook['port']}"
            
            # Construct the dictionary that holds the required data for the hook connection
            hook["address"] = hook_address
            hook.pop("port")
            
            # Update cache
            cached_hooks = Globals.cache.get("hooks")
            cached_hooks.append(hook)
            Globals.cache.set("hooks", cached_hooks)
            
            Logger.info(f"[WEBHOOK REGISTRAR] Webhook registered for the request {hook}")
            return make_response(jsonify("success"), 200)
        except Exception as ex:
            Logger.error(f"[WEBHOOK REGISTRAR] Following exception has been raised while handling the request {hook}:\n{ex}")
            return make_response(jsonify(ex), 400)
        
