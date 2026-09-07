import os
import storage
import datetime
import time
import sys

data = storage.load_data()
def show_upcoming(day_diff=0):
    sorted_tasks = sort_tasks_by_date()
    today_iso = datetime.date.today() + datetime.timedelta(7*day_diff)
    print(f"Upcoming tasks ({today_iso.strftime("%d %B %Y")} - {(today_iso + datetime.timedelta(7)).strftime("%d %B %Y")}) :")
    for i in range(7):
        view = (today_iso + datetime.timedelta(i))
        view_iso = (today_iso + datetime.timedelta(i)).isoformat()
        view_date = view.strftime("%d %B %Y").lstrip("0")
        date_task =[task for task in sorted_tasks if task["date"]==view_iso]
        if date_task:
            print(f" {view_date} :")
            local_id = 1
            for task in date_task:
                print(f" [{local_id}] {task['name']}")
                i+=1

def clear_terminal() :
    os.system("cls" if os.name == "nt" else "clear")

def sort_tasks_by_date():
    sorted_tasks = list(data["tasks"])
    n = len(sorted_tasks)
    for i in range(n):
        for j in range(n - i - 1):
            if sorted_tasks[j]["date"] > sorted_tasks[j + 1]["date"]:
                temp = sorted_tasks[j]
                sorted_tasks[j] = sorted_tasks[j + 1]
                sorted_tasks[j + 1] = temp
    return sorted_tasks

def next_handle(user_input):
    for day in range (1,8):
        target_date= datetime.date.today() + datetime.timedelta(day)
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
    print(f"It's great to see you, {data['username']} ! \n")

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

def view_task(day_diff=0):
    clear_terminal()
    show_upcoming(day_diff)
    print("="*30)
    print("1-view later tasks \n2-Back to main menu")
    view_menu = input("Command :")
    if view_menu in ["later","next","1"]:
        view_task(day_diff+1)
    else :
        clear_terminal()
        return


def new_task(supp_task_name=None):
    clear_terminal()
    if not supp_task_name is None:
        task_affirm = input(f"do you wanna add \"{supp_task_name}\" as a task ?")
        if task_affirm in affirmative :
            task_name = supp_task_name
        else:
            clear_terminal()
            return
    else :
        task_name = input("What is the task ?")
    task_date = input("Insert Date (YYYY-MM-DD) or simply type 'today',or a weekday (e.g., 'Friday') :")
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
    print("Task saved !")
    time.sleep(1)
    clear_terminal()
    return

def edit_task():
    sorted_tasks = sort_tasks_by_date()
    show_upcoming()
    print("Choose which task you want to edit:\ntype \"later\" for later tasks\ntype \"exit\" to exit ")
    edit_menu = input("Command :")

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
    while True :
        greet()
        time.sleep(1)
        today_tasks()
        show_menu()
        menu_choice = input("Command :").strip()
        execute_cmd(menu_choice)



initialize_app()

