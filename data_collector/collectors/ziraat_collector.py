from .base_collector import BaseCollector

from src.utils.globals import Globals
from src.utils.logger import Logger

from bs4 import BeautifulSoup
import requests
import datetime


class ZiraatCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__(base_container)
        
    def run(self):
        timestamp = int(datetime.datetime.now().timestamp())
        ziraat_hooks = [hook for hook in Globals.cache.get("hooks") if ("ziraat" in hook["exchanges"])]

        try:
            page = requests.get(self.config_service.ziraat_url)
            soup = BeautifulSoup(page.content, "lxml")
            
            forex_div = soup.find("div", {"class": "js-item", "data-id": "rdIntBranchDoviz"})
            forex_table = forex_div.find_all("td")
            
            live_rates = {}
            upsert_queries = []
            for currency, index in self.config_service.ziraat_rate_indices.items():
                rate = float(forex_table[index].text.replace(",", "."))
                
                cached_data = Globals.cache.get(currency)
                cached_rate = cached_data["ziraat"]
                
                if rate != cached_rate:
                    cached_data["ziraat"] = rate
                    Globals.cache.set(currency, cached_data)
                    
                    # Post webhooks
                    self.post_webhooks(
                        hooks=ziraat_hooks,
                        timestamp=timestamp,
                        exchange="ziraat",
                        buy_sell=currency[4:],
                        currency=currency[:3],
                        rate=rate
                    )
                    
                    live_rates[currency] = rate

                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{currency[:3]}', 'ziraat', '{currency[4:]}', {rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {rate};"
                    ) 
                    
            # Update websockets
            self.emit_sockets(exchange="ziraat", rates=live_rates)
            
            # Update the database
            if upsert_queries:
                self.data_service.dml(query="".join(upsert_queries)) 

        except Exception as ex:
            Logger.error(f"[Ziraat][GET] {ex}")
