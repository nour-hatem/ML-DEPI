from abc import ABC, abstractmethod
import requests

class UserDataSource(ABC):
    @abstractmethod
    def get_users():
        pass
    
class User:
    def __init__(self, name, email, city, company):
        self.name = name
        self.email = email
        self.__city = city
        self.__company = company

    def get_city(self):
        return self.__city

    def get_company(self):
        return self.__company