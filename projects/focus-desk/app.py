"""Focus Desk: a small, local-first Tkinter task app. Python 3.10+."""
import json
import os
from pathlib import Path
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk
from uuid import uuid4

DATA_PATH = Path.home() / ".focus-desk" / "tasks.json"


def load_tasks(path):
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Task data must be a list.")
    ids = set()
    for task in data:
        if (not isinstance(task, dict) or not isinstance(task.get("id"), str)
                or not task["id"] or task["id"] in ids
                or not isinstance(task.get("title"), str)
                or not task["title"].strip() or len(task["title"]) > 200
                or type(task.get("done")) is not bool):
            raise ValueError("A saved task is invalid.")
        ids.add(task["id"])
    return data


def save_tasks(path, tasks):
    """Replace the save file only after its new contents are fully written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(tasks, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


class FocusDesk:
    def __init__(self, root):
        self.root = root
        self.tasks = []
        self.root.title("Focus Desk")
        self.root.geometry("760x540")
        self.root.minsize(560, 420)
        self.root.configure(bg="#0b1220")
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("TFrame", background="#0b1220")
        style.configure("TLabel", background="#0b1220", foreground="#f1f5f9")
        style.configure("TButton", padding=9)
        style.configure("Treeview", rowheight=34, background="#142233",
                        fieldbackground="#142233", foreground="#f1f5f9")
        frame = ttk.Frame(root, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Focus Desk", font=("Segoe UI", 26, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Small steps. Clear progress. Your tasks stay on this device.").pack(anchor="w", pady=(4, 20))
        entry_row = ttk.Frame(frame)
        entry_row.pack(fill="x")
        self.entry = ttk.Entry(entry_row, font=("Segoe UI", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda event: self.add_task())
        ttk.Button(entry_row, text="Add task", command=self.add_task).pack(side="right")
        filters = ttk.Frame(frame)
        filters.pack(fill="x", pady=14)
        self.filter = tk.StringVar(value="All")
        ttk.Label(filters, text="Show:").pack(side="left", padx=(0, 10))
        for value in ("All", "Active", "Completed"):
            ttk.Radiobutton(filters, text=value, value=value, variable=self.filter,
                            command=self.refresh).pack(side="left", padx=6)
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_frame, columns=("status", "task"), show="headings", selectmode="browse")
        self.table.heading("status", text="Status")
        self.table.heading("task", text="Task")
        self.table.column("status", width=110, stretch=False)
        self.table.column("task", width=400)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.table.bind("<space>", lambda event: self.toggle_task())
        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=(16, 0))
        ttk.Button(controls, text="Complete / reopen", command=self.toggle_task).pack(side="left")
        ttk.Button(controls, text="Delete selected", command=self.delete_task).pack(side="left", padx=10)
        self.status = ttk.Label(frame, text="")
        self.status.pack(anchor="w", pady=(12, 0))
        try:
            self.tasks = load_tasks(DATA_PATH)
        except (OSError, ValueError) as error:
            messagebox.showerror("Cannot read saved tasks", f"Your saved file has been preserved.\n{DATA_PATH}\n\n{error}\n\nRepair or back up and rename it before restarting.")
            root.destroy()
            return
        self.refresh()
        self.entry.focus_set()

    def commit(self, updated):
        try:
            save_tasks(DATA_PATH, updated)
        except OSError as error:
            messagebox.showerror("Could not save", f"Your change was not saved.\n{error}")
            return False
        self.tasks = updated
        self.refresh()
        return True

    def add_task(self):
        title = self.entry.get().strip()
        if not title or len(title) > 200:
            messagebox.showinfo("Task title", "Enter a task between 1 and 200 characters.")
            return
        if self.commit(self.tasks + [{"id": uuid4().hex, "title": title, "done": False}]):
            self.entry.delete(0, "end")

    def selected_id(self):
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Select a task", "Select a task in the list first.")
            return None
        return selection[0]

    def toggle_task(self):
        task_id = self.selected_id()
        if task_id:
            self.commit([{**task, "done": not task["done"]} if task["id"] == task_id else task
                         for task in self.tasks])

    def delete_task(self):
        task_id = self.selected_id()
        if task_id and messagebox.askyesno("Delete task", "Delete the selected task?"):
            self.commit([task for task in self.tasks if task["id"] != task_id])

    def refresh(self):
        self.table.delete(*self.table.get_children())
        for task in self.tasks:
            if self.filter.get() == "Active" and task["done"]:
                continue
            if self.filter.get() == "Completed" and not task["done"]:
                continue
            self.table.insert("", "end", iid=task["id"], values=("Done" if task["done"] else "Active", task["title"]))
        completed = sum(task["done"] for task in self.tasks)
        self.status.configure(text=f"{len(self.tasks) - completed} active · {completed} completed")


if __name__ == "__main__":
    window = tk.Tk()
    FocusDesk(window)
    window.mainloop()
