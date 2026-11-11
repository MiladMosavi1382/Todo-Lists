
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_PATH = os.path.join(DATA_DIR, "task.json")


def load_tasks():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


def add_task(tasks, title):
    title = title.strip()

    if not title:
        return False

    tasks.append({
        "title": title,
        "done": False
    })

    save_tasks(tasks)
    return True


def delete_task(tasks, index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        return True

    return False


def complete_task(tasks, index):
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        return True

    return False

