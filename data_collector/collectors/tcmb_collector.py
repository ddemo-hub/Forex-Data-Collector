from .base_collector import BaseCollector

from src.utils.globals import Globals

from datetime import datetime
import requests
import pandas

class TCMBCollector(BaseCollector):
    def __init__(self, base_container):
        super().__init__(base_container)
        self.cron = self.config_service.tcmb_cron

    def run(self):
        tcmb_hooks = [hook for hook in Globals.cache.get("hooks") if ("TCMB" in hook["exchanges"])]
        
        currencies = [f"TP.DK.{currency}.A.YTL-TP.DK.{currency}.S.YTL" for currency, is_used in self.config_service.currencies.items() if is_used]
        currencies = "-".join(currencies)
        
        datetime_now = datetime.now().strftime("%d-%m-%Y")
        request = self.config_service.tcmb_api_url.format(currencies, datetime_now, datetime_now, self.config_service.tcmb_api_key)
        
        try:
            rates = pandas.read_csv(request)
            timestamp = int(datetime.strptime(rates.at[0, "Tarih"], "%d-%m-%Y").timestamp())
            
            upsert_queries = []        
            for currency in rates.columns.drop(["Tarih", "UNIXTIME"]):
                cache_key = f"TCMB_{currency[6:9]}_{'sell' if currency[10] == 'S' else 'buy'}"
                
                if Globals.cache.get(cache_key) != rates[currency].item():
                    # Update the cache if the currency's value is changed
                    Globals.cache.set(cache_key, rates[currency].item())
                    
                    # Send the new value of the currency to the hooks
                    for target_hook in [hook for hook in tcmb_hooks if (currency[6:9] in hook["currencies"])]:
                        try:
                            requests.post(url=target_hook, json={"timestamp": timestamp, currency[6:9]: rates[currency].item()})
                        except Exception as ex:
                            self.logger.error(f"[TCMBCollector][POST] {ex}")

                # Construct the query for the currency
                upsert_queries.append(
                    f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                    f"({timestamp}, '{currency[6:9]}', 'TCMB', '{'sell' if currency[10] == 'S' else 'buy'}', {rates[currency].item()}) " + \
                    f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {31};"
                )            
            
            # Update the database
            self.data_service.dml(query="".join(upsert_queries)) 
                  
        except Exception as ex:
            self.logger.error(f"[TCMBCollector][GET] {ex}")
