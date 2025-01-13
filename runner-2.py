import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

root = tk.Tk()
root.title("Weekly Planner with Themes")
root.geometry("1200x800")

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
tasks_by_day = {day: [] for day in days}
task_colors = {}
themes = {
    "Light": {"bg": "#ffffff", "fg": "#000000", "canvas_bg": "#ffffff", "timeline_fg": "#000000", "text_fg": "#000000"},
    "Dark": {"bg": "#2c2c2c", "fg": "#ffffff", "canvas_bg": "#3a3a3a", "timeline_fg": "#ffffff", "text_fg": "#ffffff"},
}
current_theme = "Dark"

def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme = themes[current_theme]
    root.config(bg=theme["bg"])
    style = ttk.Style()
    style.configure("TLabel", background=theme["bg"], foreground=theme["fg"])
    style.configure("Header.TLabel", background=theme["bg"], foreground=theme["fg"], font=("Arial", 16, "bold"))

    canvas.config(bg=theme["canvas_bg"])

def clear_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

def create_main_screen():
    clear_screen()
    ttk.Label(main_frame, text="Weekly Planner", style="Header.TLabel").pack(pady=10)
    ttk.Button(main_frame, text="Add Tasks", command=add_tasks_screen).pack(pady=5)
    ttk.Button(main_frame, text="View Weekly Schedule", command=view_weekly_schedule).pack(pady=5)
    ttk.Button(main_frame, text="Switch Theme", command=toggle_theme).pack(pady=5)
    ttk.Button(main_frame, text="Exit", command=root.quit).pack(pady=5)

def toggle_theme():
    if current_theme == "Dark":
        apply_theme("Light")
    else:
        apply_theme("Dark")
    create_main_screen()

def add_tasks_screen():
    clear_screen()
    ttk.Label(main_frame, text="Add Tasks", style="Header.TLabel").pack(pady=10)

    task_name_var = tk.StringVar()
    task_days_vars = {day: tk.BooleanVar() for day in days}
    task_start_time_var = tk.StringVar()
    task_end_time_var = tk.StringVar()

    entry = ttk.Entry(main_frame, textvariable=task_name_var)
    entry.insert(0, "Task Name")
    entry.pack(pady=5)

    ttk.Label(main_frame, text="Select Days:", style="TLabel").pack(pady=5)
    for day in days:
        ttk.Checkbutton(main_frame, text=day, variable=task_days_vars[day]).pack(anchor="w")

    start_entry = ttk.Entry(main_frame, textvariable=task_start_time_var)
    start_entry.insert(0, "Start Time (HH:MM)")
    start_entry.pack(pady=5)

    end_entry = ttk.Entry(main_frame, textvariable=task_end_time_var)
    end_entry.insert(0, "End Time (HH:MM)")
    end_entry.pack(pady=5)

    def add_task():
        name = task_name_var.get().strip()
        selected_days = [day for day, var in task_days_vars.items() if var.get()]
        start_time = task_start_time_var.get().strip()
        end_time = task_end_time_var.get().strip()

        if not name or not selected_days:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        try:
            start_hour = int(start_time.split(":")[0]) + int(start_time.split(":")[1]) / 60
            end_hour = int(end_time.split(":")[0]) + int(end_time.split(":")[1]) / 60
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid time format.")
            return

        for day in selected_days:
            if end_hour < start_hour:
                tasks_by_day[day].append({"task": name, "start_hour": start_hour, "end_hour": 24})
                next_day = days[(days.index(day) + 1) % len(days)]
                tasks_by_day[next_day].append({"task": name, "start_hour": 0, "end_hour": end_hour})
            else:
                tasks_by_day[day].append({"task": name, "start_hour": start_hour, "end_hour": end_hour})

        messagebox.showinfo("Success", "Task added successfully!")
        create_main_screen()

    ttk.Button(main_frame, text="Add", command=add_task).pack(pady=5)
    ttk.Button(main_frame, text="Back", command=create_main_screen).pack(pady=5)

def view_weekly_schedule():
    clear_screen()
    ttk.Label(main_frame, text="Weekly Schedule", style="Header.TLabel").pack(pady=10)
    global canvas
    canvas = tk.Canvas(main_frame, width=1100, height=650)
    canvas.pack(pady=10)

    theme = themes[current_theme]
    apply_theme(current_theme)

    day_width = 150
    hour_height = 25
    timeline_width = 60

    for i, day in enumerate(days):
        x = timeline_width + i * day_width
        canvas.create_text(x + day_width / 2, 20, text=day, font=("Arial", 12, "bold"), fill=theme["text_fg"])

    for hour in range(25):
        y = (hour + 1) * hour_height
        canvas.create_text(timeline_width / 2, y - 15, text=f"{hour:02}:00", font=("Arial", 10), fill=theme["text_fg"])

    default_colors = ["lightblue", "lightgreen", "lightpink", "lightcoral", "lavender", "khaki", "lightgoldenrod"]
    for i, day in enumerate(days):
        x = timeline_width + i * day_width
        for task in tasks_by_day[day]:
            start_y = (task["start_hour"] + 1) * hour_height
            end_y = (task["end_hour"] + 1) * hour_height
            if task["task"] not in task_colors:
                task_colors[task["task"]] = default_colors[len(task_colors) % len(default_colors)]
            task_color = task_colors[task["task"]]
            canvas.create_rectangle(x, start_y, x + day_width, end_y, fill=task_color, outline="black")
            canvas.create_text(x + day_width / 2, (start_y + end_y) / 2, text=task["task"], font=("Arial", 10))

    ttk.Button(main_frame, text="Back", command=create_main_screen).pack(pady=5)

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")
create_main_screen()
root.mainloop()
