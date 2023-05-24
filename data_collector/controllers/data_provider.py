from src.services.config_service import ConfigService
from src.services.data_service import DataService

from src.utils.globals import Globals

from flask import request, jsonify, make_response
from flask.views import MethodView

class DataProvider(MethodView):
    init_every_request= False
    
    def __init__(self, config_service: ConfigService, data_service: DataService):
        self.config_service = config_service
        self.data_service = data_service

    def get(self):
        json_request = request.json
        try:
            if json_request.keys() >= {"end_timestamp", "start_timestamp"}:
                try:
                    select_query = f"SELECT * FROM public.forex_rates WHERE 'currency' = '{json_request['currency']}' " + \
                                   f"AND 'exchange' = '{json_request['exchange']}' AND 'buy_sell' = '{json_request['buy_sell']}' " + \
                                   f"AND 'timestamp' BETWEEN {json_request['start_timestamp']} AND {json_request['end_timestamp']};" 
                    
                    requested_data = self.data_service.dql(query=select_query, columns=["timestamp", "currency", "exchange", "buy_sell", "rate"])
                    return make_response(requested_data.to_json(), 200)
                except Exception as ex:
                    return make_response(jsonify(ex), 400)
                
            else:
                if "end_timestamp" in json_request or "start_timestamp" in json_request:
                    return make_response(jsonify("In a valid request, 'start_timestamp' and 'end_timestamp' parameters must either be present together or neither of them should be present at all."), 400)
                
                try:            
                    cache_key = f"{json_request['exchange']}_{json_request['currency']}_{json_request['buy_sell']}"
                except KeyError:
                    return make_response(jsonify("Missing parameters in the request. Params: 'exchange', 'currency', 'buy_sell', 'start_timestamp (optional)', 'end_timestamp (optional)'"), 400)
                
                try:
                    cached_data = Globals.cache.get(cache_key)
                    return make_response(jsonify(cached_data), 200)
                except KeyError as ex:
                    if json_request['exchange'] not in self.config_service.exchanges:
                        error_message = f"The 'exchange' parameter must be either one of {self.config_service.exchanges}"
                    elif json_request['currency'] not in self.config_service.currencies.keys():
                        error_message = f"The 'currency' parameter must be either one of {self.config_service.currencies.keys()}"
                    elif json_request["buy_sell"] != "buy" and json_request["buy_sell"] != "sell":
                        error_message = f"The 'buy_sell' parameter must be either one of 'buy' or 'sell'"            
                    else: 
                        error_message = ex
                        
                    return make_response(jsonify(error_message), 400)

        except Exception as ex:
            return make_response(jsonify(ex), 400)