from .base_collector import BaseCollector

from src.utils.globals import Globals
from src.utils.logger import Logger

from datetime import datetime
import requests
import pandas

class TCMBCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__(base_container)

    def run(self):
        tcmb_hooks = [hook for hook in Globals.cache.get("hooks") if ("TCMB" in hook["exchanges"])]
        
        currencies = [f"TP.DK.{currency}.A.YTL-TP.DK.{currency}.S.YTL" for currency in self.config_service.tcmb_currencies]
        currencies = "-".join(currencies)
        
        datetime_now = datetime.now().strftime("%d-%m-%Y")
        request = self.config_service.tcmb_api_url.format(currencies, datetime_now, datetime_now, self.config_service.tcmb_api_key)
        
        try:
            rates = pandas.read_csv(request)
            timestamp = int(datetime.strptime(rates.at[0, "Tarih"], "%d-%m-%Y").timestamp())
            
            upsert_queries = []
            live_rates = {}        
            for currency in rates.columns.drop(["Tarih", "UNIXTIME"]):
                curr = currency[6:9]
                live_rate = rates[currency].item()
                is_buy_sell = 'SELL' if currency[10] == 'S' else 'BUY'
                
                live_rates[f"{curr}_{is_buy_sell}"] = live_rate
                
                cached_data = Globals.cache.get(f"{curr}_{is_buy_sell}")
                cached_rate = cached_data["TCMB"]
                
                if cached_rate != live_rate:
                    # Update the cache if the currency's value is changed
                    cached_data["TCMB"] = live_rate
                    Globals.cache.set(f"{curr}_{is_buy_sell}", cached_data)

                    # Post webhooks
                    self.post_webhooks(
                        hooks=tcmb_hooks,
                        timestamp=timestamp,
                        exchange="TCMB",
                        buy_sell=curr,
                        currency=is_buy_sell,
                        rate=live_rates
                    )
                    
                    # Construct the query for the currency
                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{curr}', 'TCMB', '{is_buy_sell}', {live_rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {live_rate};"
                    ) 

            # Update websockets
            self.emit_sockets(exchange="TCMB", rates=live_rates)

            # Update the database
            if upsert_queries:
                self.data_service.dml(query="".join(upsert_queries)) 
                    
        except Exception as ex:
            Logger.error(f"[TCMBCollector][GET] {ex}")
