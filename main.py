import os
import storage
import datetime
import time
import sys

data = storage.load_data()
affirmative = ("yes","ye","yeah","ok","y")
negative = ("no","nah","na","nope","exit","n")

def separator(user_input):
    print("="*user_input)

def show_upcoming(mode,day_diff=0):
    sorted_tasks = sort_tasks_by_date()
    today_iso = datetime.date.today() + datetime.timedelta(7*day_diff)
    print(f"Upcoming tasks ({today_iso.strftime("%d %B %Y")} - {(today_iso + datetime.timedelta(7)).strftime("%d %B %Y")}) :\n")
    local_id = 1
    displayed_tasks = []
    for i in range(7):
        view = (today_iso + datetime.timedelta(i))
        view_iso = (today_iso + datetime.timedelta(i)).isoformat()
        view_date = view.strftime("%d %B %Y").lstrip("0")
        date_task =[task for task in sorted_tasks if task["date"]==view_iso]
        if date_task:
            print(f" {view_date} :")
            for task in date_task:
                if mode =="view" :
                    print(f"   -{task['name']}")
                else:
                    print(f" [{local_id}] {task['name']}")
                    displayed_tasks.append(task)
                    local_id += 1
    print("\n"+"="*56)
    return displayed_tasks

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
        if target_date.strftime("%A") == user_input.capitalize() or target_date.strftime("%a") ==user_input.capitalize() :
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
    separator(106)
    separator(106)
    print("""
     TTTTTTTTT   AAAA    SSSSS  KK  KK    MM    MM   AAAA   NN   NN   AAAA    GGGGG  EEEEEEE RRRRRR  
        TTT     AA  AA  SS      KK KK     MMM  MMM  AA  AA  NNN  NN  AA  AA  GG   GG EE      RR   RR 
        TTT     AAAAAA   SSSSS  KKKK      MM MM MM  AAAAAA  NN N NN  AAAAAA  GG  _   EEEEE   RRRRRR  
        TTT     AA  AA       SS KK KK     MM    MM  AA  AA  NN  NNN  AA  AA  GG   GG EE      RR  RR  
        TTT     AA  AA   SSSSS  KK  KK    MM    MM  AA  AA  NN   NN  AA  AA   GGGGG  EEEEEEE RR   RR 
    """)
    separator(106)
    separator(106)
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
    while True:
        clear_terminal()
        show_upcoming("view",day_diff)
        print("[p/prev] View previous week's tasks")
        print("[n/next] View next week's tasks")
        print("[e/exit] Return to main menu")
        view_menu = input("\nCommand :").lower()
        if view_menu in ["next", "n"]:
            day_diff += 1
        elif view_menu in ["previous", "prev", "p"]:
            day_diff -= 1
        elif view_menu in ["exit", "ex", "back", "q", "e"]:
            clear_terminal()
            return
        else:
            clear_terminal()
            print("Invalid input, please try again!")
            time.sleep(1)

def new_task(supp_task_name=None):
    clear_terminal()
    if not supp_task_name is None:
        task_affirm = input(f"do you wanna add \"{supp_task_name}\" as a task ?")
        if task_affirm in affirmative :
            task_name = supp_task_name
        else:
            print("returning to main menu ..")
            time.sleep(1)
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

def edit_interface(later_count=0):
    while True :
        clear_terminal()
        displayed_tasks = show_upcoming("edit",later_count)
        print("[   #  ] Select task number to edit")
        print("[p/prev] View previous week's tasks")
        print("[n/next] View next week's tasks")
        print("[e/exit] Return to main menu")
        edit_menu = input("\nCommand :")
        if edit_menu in ["next","n"]:
            later_count+=1
        elif edit_menu in ["exit","ex","back","q","e"]:
            clear_terminal()
            return
        elif edit_menu in ["previous","prev","p"]:
            later_count-=1
        elif edit_menu.isdigit() and 0<int(edit_menu)<=len(displayed_tasks):
            edit_task(displayed_tasks,edit_menu)
        else :
            clear_terminal()
            print("Invalid input, please try again!")
            time.sleep(1)

def edit_task(displayed_tasks,task_menu_id):
    while True :
        clear_terminal()
        separator(26)
        print(f" Task name : {displayed_tasks[int(task_menu_id)-1]["name"]}\n Task date : {displayed_tasks[int(task_menu_id)-1]["date"]}\n {"Task is done" if displayed_tasks[int(task_menu_id)-1]["is_done"] else "Task is not yet finished"}")
        separator(26)
        edit_atr = input("[1] Edit name\n[2] Edit date\n[3] Edit status\n[4] Return\nCommand :")
        if edit_atr.lower() in ["1", "name", "n"]:
            displayed_tasks[int(task_menu_id) - 1]["name"] = input("New name :")
            storage.save_data(data)
            clear_terminal()
            print("Saving new task name ..")
            time.sleep(1)
        elif edit_atr.lower() in ["2", "date", "d"]:
            task_date = input("Insert Date (YYYY-MM-DD) or simply type 'today',or a weekday (e.g., 'Friday') :")
            if task_date.strip().lower() == "today":
                task_date = datetime.date.today().isoformat()
            elif next_handle(task_date):
                task_date = next_handle(task_date)
            displayed_tasks[int(task_menu_id) - 1]["date"] = task_date
            storage.save_data(data)
            clear_terminal()
            print("Saving new task date ..")
            time.sleep(1)
        elif edit_atr.lower() in ["3", "status", "s"]:
            status_check = input(f"is {displayed_tasks[int(task_menu_id) - 1]["name"]} done ?")
            if status_check in affirmative:
                displayed_tasks[int(task_menu_id) - 1]["is_done"] = True
            elif status_check in negative:
                displayed_tasks[int(task_menu_id) - 1]["is_done"] = False
            storage.save_data(data)
            clear_terminal()
            print("Saving  task status ..")
            time.sleep(1)
        elif edit_atr.lower() in ["4", "q", "r", "return", "back", "exit", "e"]:
            return
        else:
            clear_terminal()
            print("Invalid input , please try again!")
            time.sleep(1)

def del_task():
    pass

def settings():
    clear_terminal()
    separator(75)
    separator(75)
    print("""
     SSSSS  EEEEEEE TTTTTTT TTTTTTT  IIIII  NN   NN   GGGGG   SSSSS 
    SS      EE        TTT     TTT     III   NNN  NN  GG   GG SS     
     SSSSS  EEEEE     TTT     TTT     III   NN N NN  GG       SSSSS 
         SS EE        TTT     TTT     III   NN  NNN  GG   GG      SS
     SSSSS  EEEEEEE   TTT     TTT    IIIII  NN   NN   GGGGG   SSSSS 
    """)
    separator(75)
    separator(75)
    print("[1] Change username\n[2] Exit\n")
    settings_menu = input("Command :")
    if settings_menu in ["username","1","change","name"]:
        new_username = input("Your new username :").capitalize()
        confirm_username = input(f"Set {new_username} as your new username ? (y/n)")
        if confirm_username in affirmative :
            data["username"] = new_username
            storage.save_data(data)
            print(f"Your new username saved, {data["username"]}")
            time.sleep(1)
            clear_terminal()
            return
        elif confirm_username in negative:
            print("Ok, returning to main menu")
            time.sleep(1)
            clear_terminal()
            return
    elif settings_menu in ["exit","back","2","ex","q"]:
        clear_terminal()
        return

def exit_app():
    print("Goodbye ",end="",flush=True)
    # time.sleep(1)
    for char in "..!":
        print(char,end="",flush=True)
        # time.sleep(1)
    sys.exit()

commands = {
    view_task : ("1","view","show","look","see","quick"),
    new_task : ("2","new","add","create"),
    edit_interface : ("3","edit","change"),
    del_task : ("4","del","delete","remove","erase"),
    settings : ("5","set","username","user"),
    exit_app : ("6","leave","exit","bye","e")
}
lookup ={}
for func , alias in commands.items() :
    for al in alias :
        lookup[al]= func

def execute_cmd(user_input):
    cmd_parts = user_input.strip().lower().split(maxsplit=1)
    if not cmd_parts :
        return
    cmd = cmd_parts[0]
    if cmd in lookup:
        action = lookup[cmd]
        # if len(cmd_parts)>1:
        #     action(cmd_parts[1])
        # else :
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
    clear_terminal()
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

