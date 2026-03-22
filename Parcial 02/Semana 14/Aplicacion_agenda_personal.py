import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Necesario instalar: pip install tkcalendar

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("600x400")

        # --- Frame principal para la lista de eventos ---
        frame_lista = ttk.Frame(self.root)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        # TreeView para mostrar eventos
        self.tree = ttk.Treeview(frame_lista, columns=("Fecha", "Hora", "Descripción"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack(fill="both", expand=True)

        # --- Frame para entradas de datos ---
        frame_inputs = ttk.Frame(self.root)
        frame_inputs.pack(fill="x", padx=10, pady=5)

        # Etiquetas y campos
        ttk.Label(frame_inputs, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_entry = DateEntry(frame_inputs, width=12, background="darkblue", foreground="white", borderwidth=2)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Hora:").grid(row=0, column=2, padx=5, pady=5)
        self.hora_entry = ttk.Entry(frame_inputs)
        self.hora_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Descripción:").grid(row=1, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(frame_inputs, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # --- Frame para botones ---
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(fill="x", padx=10, pady=10)

        ttk.Button(frame_botones, text="Agregar Evento", command=self.agregar_evento).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Eliminar Evento Seleccionado", command=self.eliminar_evento).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Salir", command=self.root.quit).pack(side="right", padx=5)

    def agregar_evento(self):
        """Agrega un nuevo evento a la lista"""
        fecha = self.fecha_entry.get()
        hora = self.hora_entry.get()
        desc = self.desc_entry.get()

        if not hora or not desc:
            messagebox.showwarning("Campos incompletos", "Por favor ingresa la hora y la descripción.")
            return

        self.tree.insert("", "end", values=(fecha, hora, desc))
        self.hora_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def eliminar_evento(self):
        """Elimina el evento seleccionado con confirmación"""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Selección vacía", "Por favor selecciona un evento para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar el evento?")
        if confirmacion:
            self.tree.delete(seleccionado)

# --- Programa principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()