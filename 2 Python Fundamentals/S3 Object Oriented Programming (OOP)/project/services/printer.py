from datasource.base import UserDataSource

def print_users(data_source: UserDataSource):
    users = data_source.get_users()
    
    if not users:
        print("No users")
        return

    print(f"{'NAME':<25} | {'CITY':<20} | {'COMPANY'}")
    
    for user in users:
        print(f"{user.name:<25} | {user.get_city():<20} | {user.get_company()}")