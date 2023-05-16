from .base_collector import BaseCollector

from datetime import datetime
import requests
import pandas

class TCMBCollector(BaseCollector):
    def __init__(self, base_container):
        super().__init__(base_container)
        self.cron = self.config_service.tcmb_cron

    def run(self):
        currencies = [f"TP.DK.{currency}.A.YTL-TP.DK.{currency}.S.YTL" for currency, is_used in self.config_service.currencies.items() if is_used]
        currencies = "-".join(currencies)
        
        datetime_now = datetime.now().strftime("%d-%m-%Y")
        request = self.config_service.tcmb_api_url.format(currencies, datetime_now, datetime_now, self.config_service.tcmb_api_key)
        
        try:
            rates = pandas.read_csv(request)
            timestamp = int(datetime.strptime(rates.at[0, "Tarih"], "%d-%m-%Y").timestamp())
            
            upsert_queries = [
                f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                f"({timestamp}, '{currency[6:9]}', 'TCMB', '{'sell' if currency[10] == 'S' else 'buy'}', {rates[currency].item()}) " + \
                f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {31};"    
                for currency in rates.columns.drop(["Tarih", "UNIXTIME"])                 
            ]
            
            self.data_service.dml(query="".join(upsert_queries))       
                    
        except Exception as ex:
            self.logger.error(f"[TCMBCollector][GET] {ex}")
            
        for hook in self.hooks:
            try:
                requests.post(url=hook, json=rates.to_json())
            except Exception as ex:
                self.logger.error(f"[TCMBCollector][POST] {ex}")