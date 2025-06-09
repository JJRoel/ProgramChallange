import tkinter as tk

def add_task():
    """Add a new task to the 'Started' section"""
    task = task_entry.get()
    if task:
        started_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)

# Function to start dragging
def on_drag_start(event):
    widget = event.widget
    widget.drag_data = {"index": widget.nearest(event.y), "task": widget.get(widget.nearest(event.y))}

# Function to drop item into another list
def on_drop(event, source_list, target_list):
    widget = source_list
    if "task" in widget.drag_data:
        task = widget.drag_data["task"]
        target_list.insert(tk.END, task)
        widget.delete(widget.drag_data["index"])

root = tk.Tk()
root.title("To-Do List")

# Entry field for new tasks
task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=5)

# Button to add tasks to 'Started' section
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

# Function to create draggable sections
def create_section(title):
    frame = tk.Frame(root, relief=tk.RAISED, borderwidth=2)
    frame.pack(side=tk.LEFT, padx=10, pady=10)
    label = tk.Label(frame, text=title, font=("Arial", 14))
    label.pack()
    listbox = tk.Listbox(frame, width=40)
    listbox.pack()
    listbox.bind("<ButtonPress-1>", on_drag_start)  # Click to start dragging
    return frame, listbox

# Creating sections
started_frame, started_list = create_section("Started")
research_frame, research_list = create_section("Research")
progress_frame, progress_list = create_section("In Progress")
done_frame, done_list = create_section("Done")

# Enable both click-to-move & drag-and-drop
research_list.bind("<ButtonRelease-1>", lambda event: on_drop(event, started_list, research_list))
progress_list.bind("<ButtonRelease-1>", lambda event: on_drop(event, research_list, progress_list))
done_list.bind("<ButtonRelease-1>", lambda event: on_drop(event, progress_list, done_list))

root.mainloop()