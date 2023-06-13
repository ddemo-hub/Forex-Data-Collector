from .base_controller import BaseController

from src.utils.globals import Globals

from flask import request, render_template
from flask.views import MethodView

class MainController(MethodView, BaseController):
    init_every_request= False
    
    def __init__(self, base_container):
        super().__init__(base_container)
        
    def get(self):
        default_currency = "USD" 
        
        rates = [Globals.cache.get(f"{default_currency}_{buy_sell}") for buy_sell in ["BUY", "SELL"]]
        
        return render_template("main.html", currencies=self.config_service.currencies, selected_currency=default_currency, rates=rates)
    
    def post(self):
        selected_currency = request.values["currency"]
        
        rates = [Globals.cache.get(f"{selected_currency}_{buy_sell}") for buy_sell in ["BUY", "SELL"]]
        
        return render_template("main.html", currencies=self.config_service.currencies, selected_currency=selected_currency, rates=rates)