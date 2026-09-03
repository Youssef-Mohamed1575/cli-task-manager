import storage
import datetime
import time
import sys

data = storage.load_data()
def next_handle(user_input):
    for day in range (1,8):
        target_date= datetime.date.today() + datetime.timedelta(days=day)
        if target_date.strftime("%A") == user_input.capitalize() :
            return target_date.isoformat()


def max_id():
    ids =[]
    for task in data["tasks"]:
            ids.append(task["id"])
    return max(ids,default=0)


def set_username():
    username =input("Hello ! What is your name?").strip().capitalize()
    data["username"] = username
    storage.save_data(data)

def greet():
    print(f"Hello {data['username']} !")

def welcome():
    print("Welcome to the CLI Task Manager")

def today_tasks():
    today_date = datetime.date.today().strftime("%d %B %Y").lstrip("0")
    today_iso = datetime.date.today().isoformat()
    print(f"Today's tasks ({today_date}) :")
    for task in data["tasks"] :
        if task["date"] == today_iso :
            print(f"-{task['name']}")
    print("\n")

def view_task():
    pass

def new_task(supp_task_name=None):
    if not supp_task_name is None:
        task_affirm = input(f"do you wanna add \"{supp_task_name}\" as a task ?")
        if task_affirm in affirmative :
            task_name = supp_task_name
        else:
            task_name = input("What is the task ?")
    else :
        task_name = input("What is the task ?")
    task_date = input("Insert Date (YYYY-MM-DD) or simply type 'today',or a weekday (e.g., 'Friday' :")
    if task_date.strip().lower() == "today" :
        task_date = datetime.date.today().isoformat()
    elif next_handle(task_date):
        task_date=next_handle(task_date)
    new_task_data = {
        "id": max_id() + 1,
        "name": task_name.capitalize(),
        "date": task_date,
        "is_done": False
    }
    data["tasks"].append(new_task_data)
    storage.save_data(data)
    return

def edit_task():
    pass

def del_task():
    pass

def settings():
    pass

def exit_app():
    print("Goodbye ",end="",flush=True)
    time.sleep(1)
    for char in "..!":
        print(char,end="",flush=True)
        time.sleep(1)
    sys.exit()

commands = {
    view_task : ("1","view","show","look","see","quick"),
    new_task : ("2","new","add","create"),
    edit_task : ("3","edit","change"),
    del_task : ("4","del","delete","remove","erase"),
    settings : ("5","set","username","user"),
    exit_app : ("6","leave","exit","bye")
}
lookup ={}
for func , alias in commands.items() :
    for al in alias :
        lookup[al]= func

affirmative = ("yes","ye","yeah","ok","y")

negative = ("no","nah","na","nope","exit")


def execute_cmd(user_input):
    cmd_parts = user_input.strip().lower().split(maxsplit=1)
    if not cmd_parts :
        return
    cmd = cmd_parts[0]
    if cmd in lookup:
        action = lookup[cmd]
        if len(cmd_parts)>1:
            action(cmd_parts[1])
        else :
            action()
    else :
        new_task(user_input)

def show_menu():
    print("MENU".center(20,"-"))

    print("1-View tasks")
    print("2-New task")
    print("3-Edit task")
    print("4-Delete task")
    print("5-Settings")
    print("6-Exit")

def initialize_app():
    welcome()
    if data["username"] == "":
        set_username()
    greet()
    while True :
        today_tasks()
        max_id()
        show_menu()
        menu_choice = input("Command :").strip()
        execute_cmd(menu_choice)



initialize_app()

