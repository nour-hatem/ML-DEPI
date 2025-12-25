import requests
from datasource.base import UserDataSource
from models.user import User

class UserAPI(UserDataSource):
    url = "https://jsonplaceholder.typicode.com/users"

    def get_users(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            data_json = response.json()
            
            users = []
            for u in data_json:
                user_obj = User(
                    name=u['name'], 
                    email=u['email'], 
                    city=u['address']['city'], 
                    company=u['company']['name']
                )
                users.append(user_obj)
            return users
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return []

    def get_users_by_city(self, city_name):
        all_users = self.get_users()
        return [u for u in all_users if u.get_city().lower() == city_name.lower()]