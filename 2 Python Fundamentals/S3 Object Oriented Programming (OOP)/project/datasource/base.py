from abc import ABC, abstractmethod

class UserDataSource(ABC):
    @abstractmethod
    def get_users(self):
        pass