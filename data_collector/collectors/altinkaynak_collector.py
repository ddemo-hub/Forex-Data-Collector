from .base_collector import BaseCollector

from src.utils.globals import Globals
from src.utils.logger import Logger

from bs4 import BeautifulSoup
import requests
import datetime


class AltinkaynakCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__(base_container)
        
    def run(self):
        timestamp = int(datetime.datetime.now().timestamp())
        altinkaynak_hooks = [hook for hook in Globals.cache.get("hooks") if ("altinkaynak" in hook["exchanges"])]

        try:
            page = requests.get(self.config_service.altinkaynak_url)
            soup = BeautifulSoup(page.content, "lxml")
            
            forex_table = soup.find("table", {"class": "table"}).find_all("td")
            
            live_rates = {}
            upsert_queries = []
            for currency, index in self.config_service.altinkaynak_rate_indices.items():
                rate = float(forex_table[index].text)
                                
                cached_data = Globals.cache.get(currency)
                cached_rate = cached_data["altinkaynak"]
                
                if rate != cached_rate:
                    cached_data["altinkaynak"] = rate
                    Globals.cache.set(currency, cached_data)
                    
                    # Post webhooks
                    self.post_webhooks(
                        hooks=altinkaynak_hooks,
                        timestamp=timestamp,
                        exchange="altinkaynak",
                        buy_sell=currency[4:],
                        currency=currency[:3],
                        rate=rate
                    )

                    live_rates[currency] = rate
                                    
                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{currency[:3]}', 'altinkaynak', '{currency[4:]}', {rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {rate};"
                    ) 
                    
            # Update websockets
            self.emit_sockets(exchange="altinkaynak", rates=live_rates)
            
            # Update the database
            if upsert_queries:
                self.data_service.dml(query="".join(upsert_queries)) 

        except Exception as ex:
            Logger.error(f"[Altinkaynak][GET] {ex}")
