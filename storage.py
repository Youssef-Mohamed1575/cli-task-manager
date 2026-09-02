import json
import os

FILE_PATH = "tasks.json"
default_struct = {
    "username" : "",
    "tasks" : []
}

def load_data():
    if not(os.path.exists(FILE_PATH)):
        return default_struct
    try:
        with open(FILE_PATH,"r") as f :
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        return default_struct

def save_data(data):
        with open(FILE_PATH,"w") as f :
            json.dump(data,f,indent=2)
