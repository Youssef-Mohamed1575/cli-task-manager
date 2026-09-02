import json
import os

FILE_PATH = "tasks.json"
def load_tasks():
    if not(os.path.exists(FILE_PATH)):
        return[]
    try:
        with open(FILE_PATH,"r") as f :
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        return[]

def save_tasks(tasks):
        with open(FILE_PATH,"w") as f :
            json.dump(tasks,f,indent=2)
