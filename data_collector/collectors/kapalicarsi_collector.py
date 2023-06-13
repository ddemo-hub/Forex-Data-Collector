from .base_collector import BaseCollector

from src.utils.globals import Globals
from src.utils.logger import Logger

from bs4 import BeautifulSoup
import requests
import datetime


class KapaliCarsiCollector(BaseCollector):    
    def __init__(self, base_container):
        super().__init__("Kapalı Çarşı", base_container)
        
    def run(self):
        Logger.print(f"[INFO][{self.exchange}] Collector runs")
        
        timestamp = int(datetime.datetime.now().timestamp())
        
        cached_hooks = Globals.cache.get("hooks")
        kapalicarsi_hooks = [hook for hook in cached_hooks if (self.exchange in hook["exchanges"])]
        Globals.cache.set("hooks", cached_hooks)

        try:
            page = requests.get(self.config_service.kapalicarsi_url)
            self.check_response(page)
            
            soup = BeautifulSoup(page.content, "lxml")
            
            forex_table = soup.find_all("tr")
            
            live_rates = {}
            upsert_queries = []
            for currency, index in self.config_service.kapalicarsi_rate_indices.items():
                if currency[4:] == "BUY":
                    rate = float(forex_table[index].find_all("td")[1].text.replace(",", "."))
                elif currency[4:] == "SELL":
                    rate = float(forex_table[index].find_all("td")[2].text.replace(",", "."))
                                
                cached_data = Globals.cache.get(currency)
                cached_rate = cached_data[self.exchange]
                
                if rate != cached_rate:
                    cached_data[self.exchange] = rate
                    Globals.cache.set(currency, cached_data)
                    
                    # Post webhooks
                    self.post_webhooks(
                        hooks=kapalicarsi_hooks,
                        timestamp=timestamp,
                        buy_sell=currency[4:],
                        currency=currency[:3],
                        rate=rate
                    )

                    live_rates[currency] = rate
                                    
                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{currency[:3]}', '{self.exchange}', '{currency[4:]}', {rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {rate};"
                    ) 
                    
            # Update websockets
            self.emit_sockets(rates=live_rates)
            
            # Update the database
            if upsert_queries:
                self.data_service.dml(query="".join(upsert_queries)) 
                
            Logger.print(f"[INFO][{self.exchange}] Collector terminates")
        except Exception as ex:
            Logger.error(f"[{self.exchange}] {ex}")
