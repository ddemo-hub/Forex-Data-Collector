from .base_controller import BaseController

from src.utils.globals import Globals

from flask import request, jsonify, make_response
from flask.views import MethodView

class DataProvider(MethodView, BaseController):
    init_every_request= False
    
    def __init__(self, base_container):
        super().__init__(base_container)
        
    def get(self):
        json_request = request.json
        
        if json_request.keys() >= {"start_timestamp", "end_timestamp"}:
            if json_request.keys() >= {"exchange", "currency"}:
                select_query = f"SELECT * FROM public.forex_rates WHERE 'currency' = '{json_request['currency'].upper()}' " + \
                               f"AND 'exchange' = '{json_request['exchange']}' " + \
                               f"AND 'timestamp' BETWEEN {json_request['start_timestamp']} AND {json_request['end_timestamp']};" 
                                
            elif "currency" in json_request.keys():
                select_query = f"SELECT * FROM public.forex_rates WHERE 'currency' = '{json_request['currency'].upper()}' " + \
                               f"AND 'timestamp' BETWEEN {json_request['start_timestamp']} AND {json_request['end_timestamp']};" 
            
            elif "exchange" in json_request.keys():
                select_query = f"SELECT * FROM public.forex_rates WHERE 'exchange' = '{json_request['exchange']}' " + \
                               f"AND 'timestamp' BETWEEN {json_request['start_timestamp']} AND {json_request['end_timestamp']};" 

            try:
                requested_data = self.data_service.dql(query=select_query, columns=["timestamp", "currency", "exchange", "buy_sell", "rate"])
            except:
                return make_response(f"Missing parameters in the request. Params: 'exchange', 'currency', 'start_timestamp', 'end_timestamp'", 400)
                
            return make_response(requested_data.to_json(), 200)

        else:
            if json_request.keys() >= {"exchange", "currency"}:
                cached_buy = Globals.cache.get(f"{json_request['currency'].upper()}_BUY")
                cached_sell = Globals.cache.get(f"{json_request['currency'].upper()}_SELL")

                response = {"BUY": cached_buy[json_request["exchange"]], "SELL": cached_sell[json_request["exchange"]]}
                
            elif "currency" in json_request.keys():
                cached_buy = Globals.cache.get(f"{json_request['currency'].upper()}_BUY")
                cached_sell = Globals.cache.get(f"{json_request['currency'].upper()}_SELL")

                response = {"BUY": cached_buy, "SELL": cached_sell}
            
            elif "exchange" in json_request.keys():
                buy_response = {
                    f"{currency}_BUY": Globals.cache.get(f"{currency}_BUY")[json_request["exchange"]] 
                    for currency in self.config_service.currencies
                }
                sell_response = {
                    f"{currency}_SELL": Globals.cache.get(f"{currency}_SELL")[json_request["exchange"]] 
                    for currency in self.config_service.currencies
                }
                
                response = buy_response | sell_response
            
            else:
                 return make_response(f"Missing parameters in the request. Params: 'exchange', 'currency', 'start_timestamp', 'end_timestamp'", 400)
               
            return make_response(jsonify(response), 200)
