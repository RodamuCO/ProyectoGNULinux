import tkinter as tk
from tkinter import messagebox
import datetime
import json
from tkinter import ttk
from tkcalendar import Calendar


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description, deadline=None):
        """Agrega una tarea a la lista"""
        task = {
            "title": title,
            "description": description,
            "deadline": deadline if deadline else "Sin límite"
        }
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, title):
        """Elimina una tarea por su título"""
        for task in self.tasks:
            if task["title"].lower() == title.lower():
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False

    def show_report(self):
        """Devuelve las tareas para mostrar en la interfaz gráfica"""
        current_time = datetime.datetime.now()
        task_display = []

        for task in self.tasks:
            deadline_time = task["deadline"]
            if deadline_time == "Sin límite":
                task_display.append((task['title'], task['description'], deadline_time, "green"))
            else:
                deadline_time = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d %H:%M")
                if deadline_time < current_time:
                    task_display.append((task['title'], task['description'], task['deadline'], "red"))
                elif deadline_time - current_time < datetime.timedelta(minutes=30):
                    task_display.append((task['title'], task['description'], task['deadline'], "yellow"))
                else:
                    task_display.append((task['title'], task['description'], task['deadline'], "green"))
        return task_display

    def save_tasks(self):
        """Guarda las tareas en un archivo JSON"""
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        """Carga las tareas desde un archivo JSON si existe"""
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []


class TaskApp:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Administrador de Tareas")

        # Entradas de la interfaz
        self.title_label = tk.Label(root, text="Título de la tarea:")
        self.title_label.pack(padx=10, pady=5)

        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack(padx=10, pady=5)

        self.desc_label = tk.Label(root, text="Descripción de la tarea:")
        self.desc_label.pack(padx=10, pady=5)

        self.desc_entry = tk.Entry(root, width=50)
        self.desc_entry.pack(padx=10, pady=5)

        # Selector de fecha
        self.deadline_label = tk.Label(root, text="Fecha de vencimiento:")
        self.deadline_label.pack(padx=10, pady=5)

        self.calendar = Calendar(root, date_pattern="yyyy-mm-dd")
        self.calendar.pack(padx=10, pady=5)

        # Selector de hora
        self.time_frame = tk.Frame(root)
        self.time_frame.pack(padx=10, pady=5)

        self.hour_label = tk.Label(self.time_frame, text="Hora:")
        self.hour_label.pack(side=tk.LEFT, padx=5)

        self.hour_var = tk.StringVar(value="00")
        self.hour_menu = ttk.Combobox(self.time_frame, textvariable=self.hour_var, width=3, values=[f"{i:02}" for i in range(24)])
        self.hour_menu.pack(side=tk.LEFT, padx=5)

        self.minute_label = tk.Label(self.time_frame, text="Minutos:")
        self.minute_label.pack(side=tk.LEFT, padx=5)

        self.minute_var = tk.StringVar(value="00")
        self.minute_menu = ttk.Combobox(self.time_frame, textvariable=self.minute_var, width=3, values=[f"{i:02}" for i in range(60)])
        self.minute_menu.pack(side=tk.LEFT, padx=5)

        # Botones para agregar y eliminar tareas
        self.add_button = tk.Button(root, text="Agregar tarea", command=self.add_task)
        self.add_button.pack(padx=10, pady=5)

        self.remove_button = tk.Button(root, text="Eliminar tarea", command=self.remove_task)
        self.remove_button.pack(padx=10, pady=5)

        # Tabla para mostrar las tareas
        self.tasks_frame = ttk.Treeview(root, columns=("Title", "Description", "Deadline"))
        self.tasks_frame.heading("#1", text="Título")
        self.tasks_frame.heading("#2", text="Descripción")
        self.tasks_frame.heading("#3", text="Plazo")
        self.tasks_frame.pack(padx=10, pady=5)

        # Actualizar la interfaz cada 2 segundos
        self.update_task_list()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        date = self.calendar.get_date()
        hour = self.hour_var.get()
        minute = self.minute_var.get()

        if date and hour and minute:
            deadline = f"{date} {hour}:{minute}"
            try:
                deadline_time = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                self.manager.add_task(title, description, deadline)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto.")
                return
        else:
            self.manager.add_task(title, description)

        self.show_tasks()

    def remove_task(self):
        title = self.title_entry.get()

        if title:
            if self.manager.remove_task(title):
                messagebox.showinfo("Éxito", f"Tarea '{title}' eliminada.")
            else:
                messagebox.showerror("Error", f"Tarea '{title}' no encontrada.")
            self.show_tasks()

    def show_tasks(self):
        for item in self.tasks_frame.get_children():
            self.tasks_frame.delete(item)

        task_display = self.manager.show_report()

        for task in task_display:
            color = task[3]
            self.tasks_frame.insert("", "end", values=(task[0], task[1], task[2]), tags=(color,))
        self.tasks_frame.tag_configure("red", background="red", foreground="white")
        self.tasks_frame.tag_configure("yellow", background="yellow", foreground="black")
        self.tasks_frame.tag_configure("green", background="green", foreground="white")

    def update_task_list(self):
        """Actualiza la lista de tareas en tiempo real"""
        self.show_tasks()
        self.root.after(2000, self.update_task_list)  # Vuelve a llamar cada 2 segundos (2000 ms)


if __name__ == "__main__":
    manager = TaskManager()
    root = tk.Tk()
    app = TaskApp(root, manager)
    root.mainloop()
