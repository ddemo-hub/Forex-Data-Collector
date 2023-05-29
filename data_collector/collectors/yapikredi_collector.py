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
            for currency, index in self.config_service.yapikredi_rate_indices:
                rate = float(str(forex_table[index])[4:-5].replace(",", "."))
                
                live_rates[currency] = rate
                
                cached_data = Globals.cache.get(currency)
                cached_rate = cached_data["yapikredi"]
                
                if rate != cached_rate:
                    cached_data["yapikredi"] = rate
                    Globals.cache.set(currency, cached_data)
                    
                    for hook in yapikredi_hooks:
                        if currency[:3] in hook["currencies"]:
                            try:
                                requests.post(url=hook, json={"timestamp": timestamp, "exchange": "yapikredi", "buy_sell": currency[4:], currency[:3]: rate})
                            except Exception as ex:
                                Logger.error(f"[Yapı Kredi][POST] {ex}")

                    upsert_queries.append(
                        f"INSERT INTO public.forex_rates (timestamp, currency, exchange, buy_sell, rate) VALUES " + \
                        f"({timestamp}, '{currency[:3]}', 'yapikredi', '{currency[4:]}', {rate}) " + \
                        f"ON CONFLICT (timestamp, currency, exchange, buy_sell) DO UPDATE SET rate = {rate};"
                    ) 
                    
            # Update websockets
            Globals.socketio.emit("update_rates", {"exchange": "yapikredi", "rates": live_rates})
            
            # Update the database
            self.data_service.dml(query="".join(upsert_queries)) 
        
        except Exception as ex:
            Logger.error(f"[Yapı Kredi][GET] {ex}")
