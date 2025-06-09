import tkinter as tk
from tkinter import messagebox
import json

# Suppress deprecation warning for older macOS versions
TK_SILENCE_DEPRECATION = 1

class LoginSystem:
    """Handles the user login functionality."""
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x150")  # Set a fixed size for the login window
        self.root.resizable(False, False)  # Prevent resizing login window

        # Authorized users
        self.authorized_users = {
            "simon": "051168",
            "jorrit": "16102003"
        }

        # Login frame
        self.login_frame = tk.Frame(self.root, padx=10, pady=10)
        self.login_frame.pack(expand=True)

        # Username Label and Entry
        tk.Label(self.login_frame, text="Gebruikersnaam").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.user_entry = tk.Entry(self.login_frame, width=25)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.user_entry.focus_set()

        # Code Label and Entry
        tk.Label(self.login_frame, text="Wachtwoord:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.code_entry = tk.Entry(self.login_frame, width=25, show="*")
        self.code_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button
        login_button = tk.Button(self.login_frame, text="Login", command=self.check_credentials)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Bind 'Enter' key to login function
        self.root.bind('<Return>', self.check_credentials)

    def check_credentials(self, event=None):
        """Checks if the entered username and code are valid."""
        username = self.user_entry.get().lower()
        code = self.code_entry.get()

        if self.authorized_users.get(username) == code:
            self.launch_todo_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or code.")
            self.code_entry.delete(0, tk.END)

    def launch_todo_app(self):
        """Destroys login widgets and launches the main application."""
        self.login_frame.destroy()
        self.root.resizable(True, True)
        self.root.geometry("")
        TodoApp(self.root)

class TodoApp:
    """The main To-Do List application."""
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Lijst")

        # Task entry
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10, padx=10)
        self.task_entry.focus_set()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        add_button = tk.Button(button_frame, text="Toevoegen taak", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)

        complete_button = tk.Button(button_frame, text="Taak beeindigd", command=self.complete_task)
        complete_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Taak verwijderen", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)

        # Task list
        self.task_list = tk.Listbox(root, width=50, height=15)
        self.task_list.pack(pady=10, padx=10)
        self.task_list.config(font=('Helvetica', 10))  # Apply font globally

        self.load_tasks()

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

        self.update_listbox()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f, indent=4)

    def update_listbox(self):
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            display_text = task["text"]
            self.task_list.insert(tk.END, display_text)
            if task["completed"]:
                self.task_list.itemconfig(i, {'fg': 'gray'})  # Remove 'font' option
            else:
                self.task_list.itemconfig(i, {'fg': 'black'})  # Remove 'font' option

    def add_task(self):
        task_text = self.task_entry.get()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            self.save_tasks()
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def complete_task(self):
        try:
            selected_task_index = self.task_list.curselection()[0]
            self.tasks[selected_task_index]["completed"] = not self.tasks[selected_task_index]["completed"]
            self.save_tasks()
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to complete.")

    def delete_task(self):
        try:
            selected_task_index = self.task_list.curselection()[0]
            del self.tasks[selected_task_index]
            self.save_tasks()
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    login_system = LoginSystem(root)
    root.mainloop()
