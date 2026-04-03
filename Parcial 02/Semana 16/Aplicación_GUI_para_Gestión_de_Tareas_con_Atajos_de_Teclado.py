import tkinter as tk
from tkinter import messagebox

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("400x400")

        # Campo de entrada
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_task)  # Atajo: Enter

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.add_btn = tk.Button(btn_frame, text="Añadir", command=self.add_task)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.complete_btn = tk.Button(btn_frame, text="Completar", command=self.complete_task)
        self.complete_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Eliminar", command=self.delete_task)
        self.delete_btn.grid(row=0, column=2, padx=5)

        # Lista de tareas
        self.listbox = tk.Listbox(root, width=50, height=15)
        self.listbox.pack(pady=10)

        # Atajos de teclado
        self.root.bind("<c>", self.complete_task)   # Atajo: C
        self.root.bind("<d>", self.delete_task)     # Atajo: D
        self.root.bind("<Delete>", self.delete_task) # Atajo: Delete
        self.root.bind("<Escape>", lambda e: root.quit()) # Atajo: Escape

        # Diccionario para estado de tareas
        self.tasks = {}

    def add_task(self, event=None):
        task = self.entry.get().strip()
        if task:
            self.listbox.insert(tk.END, task)
            self.tasks[task] = False  # False = pendiente
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Aviso", "La tarea no puede estar vacía.")

    def complete_task(self, event=None):
        try:
            index = self.listbox.curselection()[0]
            task = self.listbox.get(index)
            if not self.tasks[task]:
                self.tasks[task] = True
                self.listbox.delete(index)
                self.listbox.insert(index, f"[✔] {task}")
            else:
                messagebox.showinfo("Info", "La tarea ya está completada.")
        except IndexError:
            messagebox.showwarning("Aviso", "Selecciona una tarea primero.")

    def delete_task(self, event=None):
        try:
            index = self.listbox.curselection()[0]
            task = self.listbox.get(index)
            self.listbox.delete(index)
            del self.tasks[task.replace("[✔] ", "")]
        except IndexError:
            messagebox.showwarning("Aviso", "Selecciona una tarea primero.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
