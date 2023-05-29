from src.utils.singleton import Singleton

import pathlib
import uuid
import yaml
import os

class ConfigService(metaclass=Singleton):
    def __init__(self, configs: pathlib.Path):
        self.config = {} 

        # Append the contents of every .yaml file in configs directory into self.config dictionary 
        for config_file in os.listdir(configs):
            config_name = config_file[:-5]  # Remove .yaml suffix
            config_path = configs.joinpath(config_file) 
            
            with open(config_path, "r") as cf:
                self.config[config_name] = yaml.safe_load(cf)
                   
    @property
    def postgres_user(self):
        return self.config["dbms"]["PostgreSQL"]["user"] 
    
    @property
    def postgres_password(self):
        return self.config["dbms"]["PostgreSQL"]["password"] 
    
    @property
    def postgres_host(self):
        return self.config["dbms"]["PostgreSQL"]["host"] 
    
    @property
    def postgres_port(self):
        return self.config["dbms"]["PostgreSQL"]["port"] 
    
    @property
    def postgres_database(self):
        return self.config["dbms"]["PostgreSQL"]["database"] 

    @property
    def postgres_execute_schema(self):
        return self.config["dbms"]["PostgreSQL"]["execute_schema"]
    
    @property
    def secret_key(self):
        secret_key = self.config["service"]["secret_key"]
        return secret_key if secret_key is not None else uuid.uuid4().hex
    
    @property
    def host(self):
        return self.config["service"]["host"]

    @property
    def port(self):
        return self.config["service"]["port"]

    @property
    def currencies(self):
        return self.config["collectors"]["currencies"]

    @property
    def exchanges(self):
        return self.config["collectors"]["exchanges"]

    @property
    def tcmb_api_url(self):
        return self.config["collectors"]["tcmb_collector"]["api_url"]

    @property
    def tcmb_api_key(self):
        return self.config["collectors"]["tcmb_collector"]["api_key"]

    @property
    def tcmb_cron(self):
        return self.config["collectors"]["tcmb_collector"]["cron"]

    @property
    def yapikredi_url(self):
        return self.config["collectors"]["yapikredi"]["url"]
    
    @property
    def yapikredi_rate_indices(self):
        return self.config["collectors"]["yapikredi"]["rate_indices"]