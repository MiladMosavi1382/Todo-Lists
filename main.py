
import tkinter as tk
from tkinter import ttk, messagebox

from tasks import (
    load_tasks,
    add_task,
    delete_task,
    complete_task
)


# Main window
root = tk.Tk()
root.title("To-Do List | Task Manager")
root.geometry("750x550")
root.minsize(650, 450)
root.configure(bg="#F3F4F6")

tasks = load_tasks()


# Styles
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    font=("Tahoma", 11),
    rowheight=35,
    background="white",
    fieldbackground="white"
)

style.configure(
    "Treeview.Heading",
    font=("Tahoma", 10, "bold"),
    background="#E5E7EB"
)


# Header
header = tk.Label(
    root,
    text="TO-DO LIST",
    font=("Arial", 24, "bold"),
    bg="#F3F4F6",
    fg="#2563EB"
)
header.pack(pady=20)


subtitle = tk.Label(
    root,
    text="Manage your daily tasks easily",
    font=("Arial", 11),
    bg="#F3F4F6",
    fg="#6B7280"
)
subtitle.pack()


# Input section
input_frame = tk.Frame(root, bg="#F3F4F6")
input_frame.pack(fill="x", padx=35, pady=25)

task_entry = tk.Entry(
    input_frame,
    font=("Tahoma", 12),
    relief="solid",
    bd=1
)
task_entry.pack(side="left", fill="x", expand=True, ipady=10)


# Task table
table_frame = tk.Frame(root, bg="#F3F4F6")
table_frame.pack(fill="both", expand=True, padx=35)

columns = ("number", "title", "status")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("number", text="No.")
tree.heading("title", text="Task")
tree.heading("status", text="Status")

tree.column("number", width=60, anchor="center")
tree.column("title", width=400, anchor="center")
tree.column("status", width=150, anchor="center")

tree.pack(fill="both", expand=True)


# Counter
counter = tk.Label(
    root,
    text="Total tasks: 0",
    font=("Arial", 10, "bold"),
    bg="#F3F4F6",
    fg="#374151"
)
counter.pack(pady=10)


# Refresh task list
def refresh_tasks():
    for item in tree.get_children():
        tree.delete(item)

    for index, task in enumerate(tasks):
        status = "Completed" if task["done"] else "Pending"

        tree.insert(
            "",
            "end",
            iid=str(index),
            values=(index + 1, task["title"], status)
        )

    completed = sum(1 for task in tasks if task["done"])

    counter.config(
        text=f"Total tasks: {len(tasks)} | Completed: {completed}"
    )


# Add task
def add_new_task():
    title = task_entry.get()

    if add_task(tasks, title):
        task_entry.delete(0, tk.END)
        refresh_tasks()
    else:
        messagebox.showwarning(
            "Warning",
            "Please enter a task title!"
        )


# Get selected task
def get_selected_task():
    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a task first!"
        )
        return None

    return int(selected[0])


# Delete task
def remove_task():
    index = get_selected_task()

    if index is None:
        return

    if messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete this task?"
    ):
        delete_task(tasks, index)
        refresh_tasks()


# Complete task
def mark_completed():
    index = get_selected_task()

    if index is None:
        return

    if tasks[index]["done"]:
        messagebox.showinfo(
            "Information",
            "This task is already completed!"
        )
        return

    complete_task(tasks, index)
    refresh_tasks()


# Buttons
button_frame = tk.Frame(root, bg="#F3F4F6")
button_frame.pack(pady=20)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    command=add_new_task,
    bg="#2563EB",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=9,
    cursor="hand2"
)
add_button.pack(side="right", padx=(10, 0))


complete_button = tk.Button(
    button_frame,
    text="Complete Task",
    command=mark_completed,
    bg="#16A34A",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)
complete_button.pack(side="left", padx=8)


delete_button = tk.Button(
    button_frame,
    text="Delete Task",
    command=remove_task,
    bg="#DC2626",
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)
delete_button.pack(side="left", padx=8)


# Enter key support
task_entry.bind("<Return>", lambda event: add_new_task())


# Initial display
refresh_tasks()

root.mainloop()

