
from abc import ABC, abstractmethod

class db_client(ABC):
    def __init__(self,connection_datas:dict):
        self.connection_datas = connection_datas


    @abstractmethod
    def connect(self):
        """db's connector"""
    
    @abstractmethod
    def disconnect(self):
        """db would be disconnected"""
    
    @abstractmethod
    def query(self, query_tmp:str):
        """db query api"""
    
    @abstractmethod
    def write_data(self,data):
        """write db data"""
    
    @abstractmethod
    def describe(self):
        pass
