import requests
from datasource.user_api import UserAPI
from services.printer import print_users

def main():
    try:
        source = UserAPI()
        print_users(source)

    except requests.exceptions.ConnectionError as e:
        print("ConnectionError: ", e)
    except Exception as e:
        print(f"Another error: ", e)

if __name__ == "__main__":
    main()