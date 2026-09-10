import os
import storage
import datetime
import time
import sys

data = storage.load_data()
affirmative = ("yes","ye","yeah","ok","y")
negative = ("no","nah","na","nope","exit","n")
exit_cmd = ("q", "c", "e" , "exit", "cancel", "back", "return")
next_cmd = ("next", "n")
prev_cmd = ("previous", "prev", "pre", "p")

def separator(width,lines=1):
    for _ in range(lines):
        print("=" * width)

def show_upcoming(mode,day_diff=0):
    sorted_tasks = sort_tasks_by_date()
    today_iso = datetime.date.today() + datetime.timedelta(7*day_diff)
    print(f"Upcoming tasks ({today_iso.strftime('%d %B %Y')} - {(today_iso + datetime.timedelta(7)).strftime('%d %B %Y')}) :\n")
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
                    print(f"   -{task['name']} {'(done)' if task['is_done'] else ''}")
                else:
                    print(f" [{local_id}] {task['name']} {'(done)' if task['is_done'] else ''}")
                    displayed_tasks.append(task)
                    local_id += 1
    print()
    separator(56)
    return displayed_tasks

def clear_terminal() :
    os.system("cls" if os.name == "nt" else "clear")

def sort_tasks_by_date():
    #time comp = N^2
    #====================================================================
    # sorted_tasks = list(data["tasks"])
    # n = len(sorted_tasks)
    # for i in range(n):
    #     for j in range(n - i - 1):
    #         if sorted_tasks[j]["date"] > sorted_tasks[j + 1]["date"]:
    #             temp = sorted_tasks[j]
    #             sorted_tasks[j] = sorted_tasks[j + 1]
    #             sorted_tasks[j + 1] = temp
    #====================================================================
    # time comp = n log n
    return sorted(data["tasks"], key=lambda task: task["date"])

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
def answer_yn(question):
    answer = input(f"{question}? (y/n)").strip().lower()
    while True :
        if answer in affirmative :
            return True
        elif answer in negative :
            return False
        else:
            answer = input("please answer in (y/n)!")

def validate_date():
    correct_format = ""
    print(f"Insert Date (YYYY-MM-DD) or simply type 'today',or a weekday (e.g., 'Friday','Fri')\n[c/cancel] to return")
    task_date = input("Input :").strip().lower()
    if task_date in exit_cmd :
        return "cancel"
    if task_date == "today":
        correct_format = datetime.date.today().isoformat()
        return correct_format
    elif next_handle(task_date):
        correct_format = next_handle(task_date)
        return  correct_format
    for frmat in ("%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            correct_format = datetime.datetime.strptime(task_date, frmat).date()
            return correct_format.isoformat()
        except ValueError:
            continue
    return None

def set_username():
    username =input("Hello! What is your name?").strip().capitalize()
    data["username"] = username
    storage.save_data(data)

def greet():
    print(f"It's great to see you, {data['username']}! \n")

def welcome():
    separator(106,2)
    print("""
     TTTTTTTTT   AAAA    SSSSS  KK  KK    MM    MM   AAAA   NN   NN   AAAA    GGGGG  EEEEEEE RRRRRR  
        TTT     AA  AA  SS      KK KK     MMM  MMM  AA  AA  NNN  NN  AA  AA  GG   GG EE      RR   RR 
        TTT     AAAAAA   SSSSS  KKKK      MM MM MM  AAAAAA  NN N NN  AAAAAA  GG  _   EEEEE   RRRRRR  
        TTT     AA  AA       SS KK KK     MM    MM  AA  AA  NN  NNN  AA  AA  GG   GG EE      RR  RR  
        TTT     AA  AA   SSSSS  KK  KK    MM    MM  AA  AA  NN   NN  AA  AA   GGGGG  EEEEEEE RR   RR 
    """)
    separator(106,2)
    print("Welcome to the CLI Task Manager")

def today_tasks():
    today_date = datetime.date.today().strftime("%d %B %Y").lstrip("0")
    today_iso = datetime.date.today().isoformat()
    print(f"Today's tasks ({today_date}) :")
    for task in data["tasks"] :
        if task["date"] == today_iso :
            print(f" -{task['name']} {'(done)' if task['is_done'] else ''}")
    print("\n")

def view_task(day_diff=0):
    while True:
        clear_terminal()
        show_upcoming("view",day_diff)
        print("[p/prev] View previous week's tasks")
        print("[n/next] View next week's tasks")
        print("[e/exit] Return to main menu")
        view_menu = input("\nCommand :").lower()
        if view_menu in next_cmd:
            day_diff += 1
        elif view_menu in prev_cmd:
            day_diff -= 1
        elif view_menu in exit_cmd:
            clear_terminal()
            return
        else:
            clear_terminal()
            print("Invalid input, please try again!")
            time.sleep(1)

def new_task(supp_task_name=None):
    clear_terminal()
    if not supp_task_name is None:
        task_affirm = answer_yn(f"Add \"{supp_task_name}\" as a task")
        if task_affirm :
            task_name = supp_task_name
        else:
            print("returning to main menu ..")
            time.sleep(1)
            clear_terminal()
            return
    else :
        task_name = input("What is the task?")
    while True:
        task_date = validate_date()
        if task_date == "cancel":
            print("Task creation canceled.")
            time.sleep(1)
            clear_terminal()
            return
        if task_date:
            break
        clear_terminal()
        print("Invalid date format, please try again!")
        time.sleep(1)
        clear_terminal()
    new_task_data = {
        "id": max_id() + 1,
        "name": task_name.strip().capitalize(),
        "date": task_date,
        "is_done": False
    }
    data["tasks"].append(new_task_data)
    storage.save_data(data)
    print("Task saved!")
    time.sleep(1)
    clear_terminal()
    return
def edit_interface():
    edit_del_interface("edit")
def del_interface():
    edit_del_interface("delete")

def edit_del_interface(mode,later_count=0):
    while True :
        clear_terminal()
        displayed_tasks = show_upcoming(mode,later_count)
        if mode == "edit":
            print("[   #  ] Select task number to edit")
        elif mode == "delete":
            print("[   #  ] Select task number to delete")
        print("[p/prev] View previous week's tasks")
        print("[n/next] View next week's tasks")
        print("[e/exit] Return to main menu")
        edit_del_menu = input("\nCommand :").strip().lower()
        if edit_del_menu in next_cmd:
            later_count+=1
        elif edit_del_menu in exit_cmd:
            clear_terminal()
            return
        elif edit_del_menu in prev_cmd:
            later_count-=1
        elif edit_del_menu.isdigit() and 0<int(edit_del_menu)<=len(displayed_tasks):
            if mode == "edit" :
                edit_task(displayed_tasks,edit_del_menu)
            elif mode == "delete":
                org_ind = displayed_tasks[int(edit_del_menu)-1]["id"]
                del_task(org_ind)
        else :
            clear_terminal()
            print("Invalid input, please try again!")
            time.sleep(1)

def edit_task(displayed_tasks,task_menu_id):
    task = displayed_tasks[int(task_menu_id)-1]
    while True :
        clear_terminal()
        separator(26)
        print(f" Task name : {task['name']}\n Task date : {task['date']}\n {'Task is done' if task['is_done'] else 'Task is not yet finished'}")
        separator(26)
        edit_atr = input("[1] Edit name\n[2] Edit date\n[3] Edit status\n[e/exit] Return to tasks menu\nCommand :").strip().lower()
        if edit_atr in ["1", "name", "n"]:
            task["name"] = input("New name :").strip().capitalize()
            storage.save_data(data)
            clear_terminal()
            print("Saving new task name ..")
            time.sleep(1)
        elif edit_atr in ["2", "date", "d"]:
            while True:
                task_date = validate_date()
                if task_date == "cancel":
                    print("Date editing canceled.")
                    time.sleep(1)
                    clear_terminal()
                    task_date = task["date"]
                    break
                if task_date:
                    break
                clear_terminal()
                print("Invalid date format, please try again!")
                time.sleep(1)
                clear_terminal()
            if task_date == task["date"]:
                pass
            else:
                task["date"] = task_date
                storage.save_data(data)
                clear_terminal()
                print("Saving new task date ..")
                time.sleep(1)
        elif edit_atr in ["3", "status", "s"]:
            status_check = answer_yn(f"Mark {task['name']} as done")
            task["is_done"] = status_check
            storage.save_data(data)
            clear_terminal()
            print("Saving  task status ..")
            time.sleep(1)
        elif edit_atr in exit_cmd:
            clear_terminal()
            return
        else:
            clear_terminal()
            print("Invalid input, please try again!")
            time.sleep(1)

def del_task(index):
    task_name = ""
    for task in data["tasks"]:
        if task["id"] == index: task_name = task["name"]
    clear_terminal()
    del_confirm = answer_yn(f"Are you sure you want to delete \"{task_name}\"")
    if del_confirm :
        data["tasks"] = [task for task in data["tasks"] if task["id"] != index]
        storage.save_data(data)
        clear_terminal()
        print("Task deleted successfully!")
        time.sleep(1)
        return
    elif not del_confirm :
        clear_terminal()
        print("Deletion cancelled")
        time.sleep(1)
        return


def delete_previous_tasks():
    clear_terminal()
    today_iso = datetime.date.today().isoformat()
    past_tasks = [task for task in data["tasks"] if task["date"] < today_iso]

    if not past_tasks:
        print("No previous tasks found to delete!")
        time.sleep(1)
        return

    confirm = answer_yn(f"Delete all {len(past_tasks)} past task(s)")
    if confirm:
        # Keep only today's tasks and future tasks
        data["tasks"] = [task for task in data["tasks"] if task["date"] >= today_iso]
        storage.save_data(data)
        clear_terminal()
        print("All previous tasks deleted successfully!")
        time.sleep(1)
    else:
        print("Deletion cancelled.")

        time.sleep(1)

def delete_finished_tasks():
    clear_terminal()
    today_iso = datetime.date.today().isoformat()
    done_tasks = [task for task in data["tasks"] if task["is_done"] ]

    if not done_tasks:
        print("No completed tasks found to delete!")
        time.sleep(1)
        return

    confirm = answer_yn(f"Delete all {len(done_tasks)} done task(s)")
    if confirm:
        data["tasks"] = [task for task in data["tasks"] if not task["is_done"]]
        storage.save_data(data)
        clear_terminal()
        print("All completed tasks deleted successfully!")
        time.sleep(1)
    else:
        print("Deletion cancelled.")
        time.sleep(1)

def settings():
    clear_terminal()
    separator(75,2)
    print("""
     SSSSS  EEEEEEE TTTTTTT TTTTTTT  IIIII  NN   NN   GGGGG   SSSSS 
    SS      EE        TTT     TTT     III   NNN  NN  GG   GG SS     
     SSSSS  EEEEE     TTT     TTT     III   NN N NN  GG       SSSSS 
         SS EE        TTT     TTT     III   NN  NNN  GG   GG      SS
     SSSSS  EEEEEEE   TTT     TTT    IIIII  NN   NN   GGGGG   SSSSS 
    """)
    separator(75,2)
    print("[1] Change username\n[2] Delete all previous tasks\n[3] Delete all completed tasks\n[e/exit] Return to main menu\n")
    settings_menu = input("Command :").strip().lower()
    if settings_menu in ["username","1","change","name"]:
        new_username = input("Your new username :").capitalize()
        confirm_username = answer_yn(f"Set {new_username} as your new username")
        if confirm_username :
            data["username"] = new_username
            storage.save_data(data)
            print(f"Your new username saved, {data['username']}")
            time.sleep(1)
            clear_terminal()
            return
        elif not confirm_username:
            print("Ok, returning to main menu")
            time.sleep(1)
            clear_terminal()
            return
    elif settings_menu in ("2","pre","prev"):
        delete_previous_tasks()
    elif settings_menu in ("3","done"):
        delete_finished_tasks()
    elif settings_menu in exit_cmd:
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
    del_interface : ("4","del","delete","remove","erase"),
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
        #Might add blind actions
        action = lookup[cmd]
        action()
    else :
        new_task(user_input)

def show_menu():
    print("MENU".center(20,"-"))

    print("[1] View tasks")
    print("[2] New task")
    print("[3] Edit task")
    print("[4] Delete task")
    print("[5] Settings")
    print("[e/exit] Exit")

def initialize_app():
    clear_terminal()
    welcome()
    if data["username"] == "":
        set_username()
    while True :
        greet()
        today_tasks()
        show_menu()
        menu_choice = input("Command :").strip()
        execute_cmd(menu_choice)
        clear_terminal()

if __name__ == "__main__":
    initialize_app()

