from .base_controller import BaseController

from src.utils.globals import Globals

from flask import request, jsonify, make_response
from flask.views import MethodView

class DataProvider(MethodView, BaseController):
    init_every_request= False
    
    def __init__(self, base_container):
        super().__init__(base_container)
        
    def get(self):
        def error_message(): 
            if json_request['exchange'] not in self.config_service.exchanges:
                error_message = f"The 'exchange' parameter must be either one of {self.config_service.exchanges}"
            elif json_request['currency'] not in self.config_service.currencies:
                error_message = f"The 'currency' parameter must be either one of {self.config_service.currencies}"
            elif json_request["buy_sell"] != "BUY" and json_request["buy_sell"] != "SELL":
                error_message = f"The 'buy_sell' parameter must be either one of 'BUY' or 'SELL'"            
            else: 
                error_message = ex
        
            return error_message
        
            
        json_request = request.json
        if not json_request.keys() >= {"exchange", "currency", "buy_sell"}:
            return make_response(jsonify("Missing parameters in the request. Params: 'exchange', 'currency', 'buy_sell', 'start_timestamp (optional)', 'end_timestamp (optional)'"), 400)
        
        try:
            if json_request.keys() >= {"end_timestamp", "start_timestamp"}:
                try:
                    select_query = f"SELECT * FROM public.forex_rates WHERE 'currency' = '{json_request['currency'].upper()}' " + \
                                   f"AND 'exchange' = '{json_request['exchange']}' AND 'buy_sell' = '{json_request['buy_sell'].upper()}' " + \
                                   f"AND 'timestamp' BETWEEN {json_request['start_timestamp']} AND {json_request['end_timestamp']};" 
                    
                    requested_data = self.data_service.dql(query=select_query, columns=["timestamp", "currency", "exchange", "buy_sell", "rate"])
                    return make_response(requested_data.to_json(), 200)
                except Exception as ex:
                    return make_response(jsonify(error_message()), 400)
                
            else:
                if "end_timestamp" in json_request or "start_timestamp" in json_request:
                    return make_response(jsonify("In a valid request, 'start_timestamp' and 'end_timestamp' parameters must either be present together or neither of them should be present at all."), 400)
                
                try:
                    cached_data = Globals.cache.get(f"{json_request['currency'].upper()}_{json_request['buy_sell'].upper()}")
                    rate = cached_data[json_request['exchange']]
                    return make_response(jsonify(rate), 200)
                except KeyError as ex:
                    return make_response(jsonify(error_message()), 400)

        except Exception as ex:
            return make_response(jsonify(ex), 400)