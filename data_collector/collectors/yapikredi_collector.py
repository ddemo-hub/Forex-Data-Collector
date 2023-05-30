from .base_collector import BaseCollector

from src.utils.globals import Globals
from src.utils.logger import Logger

from bs4 import BeautifulSoup
import requests
import datetime


class YapiKrediCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__(base_container)

    def run(self):
        timestamp = int(datetime.datetime.now().timestamp())
        yapikredi_hooks = [hook for hook in Globals.cache.get("hooks") if ("yapikredi" in hook["exchanges"])]
        
        try:
            page = requests.get(self.config_service.yapikredi_url)
            soup = BeautifulSoup(page.content, "lxml")
            
            forex_table = soup.find_all("td")
            
            live_rates = {}
            upsert_queries = []
            for currency, index in self.config_service.yapikredi_rate_indices.items():
                rate = float(forex_table[index].text.replace(",", "."))
                
                cached_data = Globals.cache.get(currency)
                cached_rate = cached_data["yapikredi"]
                
                if rate != cached_rate:
                    cached_data["yapikredi"] = rate
                    Globals.cache.set(currency, cached_data)
                    
                    # Post webhooks
                    self.post_webhooks(
                        hooks=yapikredi_hooks,
                        timestamp=timestamp,
                        exchange="yapikredi",
                        buy_sell=currency[4:],
                        currency=currency[:3],
                        rate=rate
                    )
                    
                    live_rates[currency] = rate
                    
                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{currency[:3]}', 'yapikredi', '{currency[4:]}', {rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {rate};"
                    ) 
                    
            # Update websockets
            self.emit_sockets(exchange="yapikredi", rates=live_rates)
            
            # Update the database
            if upsert_queries:
                self.data_service.dml(query="".join(upsert_queries)) 
            
        except Exception as ex:
            Logger.error(f"[Yapı Kredi][GET] {ex}")
