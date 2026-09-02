import storage

data = storage.load_data()


def set_username():
    username =input("Hello ! What is your name?").strip().capitalize()
    data["username"] = username
    storage.save_data(data)
    greet()

def greet():
    print(f"Hello {data['username']} !")

def welcome():
    print("Welcome to the CLI Task Manager")

def today_tasks():
    print("Today's tasks :")
    print("\n")
def show_menu():
    print("MENU")
    print("\n")

def initialize_app():
    welcome()
    if data["username"] == "":
        set_username()
    else :
        greet()
    today_tasks()
    show_menu()
initialize_app()