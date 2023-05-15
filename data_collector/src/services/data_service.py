from src.utils.singleton import Singleton
from src.utils.globals import Globals
from src.utils.logger import Logger

from .config_service import ConfigService

import psycopg2
import pandas
import re

class DataService(metaclass=Singleton):
    def __init__(self, config_service: ConfigService):
        self.config_service = config_service
        self.connection = None
        
        self.__execute_schema()
        
    def __execute_schema(self):
        """ 
            Parse .sql file and execute the statements 
            SQL statements must end with a semicolon
        """
        connection = psycopg2.connect(
            host=self.config_service.mysql_host,
            user=self.config_service.mysql_user,
            password=self.config_service.mysql_password
        )
        cursor = connection.cursor()

        with open(Globals.db_schema_path, "r") as file:
            schema = file.read()
            statements = schema.split(";")

            for statement in statements:
                statement = re.sub("\n", "", statement)
                try:
                    cursor.execute(f"{statement};")
                    connection.commit()
                except:
                    pass
        
        cursor.close()
        connection.close()
        
    def __connect(self):
        self.connection = psycopg2.connect(
            user=self.config_service.postgres_user,
            password=self.config_service.postgres_password,
            host=self.config_service.postgres_host,
            port=self.config_service.postgres_port,
            database=self.config_service.postgres_database
        )
        
    def __disconnect(self):
        self.connection.close()
        self.connection = None
        
    def dml(self, query: str):
        """ Insert, Detele, Update Operations """
        self.__connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query=query)

            self.connection.commit()

        except Exception as ex:
            Logger.error(f"[ERROR][dml] While executing the query {query}, the following exception raised:\n{ex}")
            return 0
        
        finally:
            self.__disconnect()
            return 1
        
    def dql(self, query: str, columns: list):
        """ Select Operation """
        self.__connect()    
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query=query)
                records = cursor.fetchall()

                df_table = pandas.DataFrame(records, columns=columns)

        except Exception as ex:
            Logger.error(f"[ERROR][dql] While executing the query {query}, the following exception raised:\n{ex}")
            return 0
        
        finally:
            self.__disconnect()
            return df_table
