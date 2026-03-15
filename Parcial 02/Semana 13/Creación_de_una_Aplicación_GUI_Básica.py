import tkinter as tk
from tkinter import messagebox

# -------------------------------
# Aplicación GUI Básica con Tkinter
# -------------------------------

def agregar_dato():
    """Agrega el texto ingresado en el campo a la lista."""
    dato = entrada.get().strip()
    if dato:  # Validar que no esté vacío
        lista.insert(tk.END, dato)
        entrada.delete(0, tk.END)  # Limpiar campo de texto
    else:
        messagebox.showwarning("Advertencia", "El campo está vacío. Ingresa un dato.")

def limpiar_dato():
    """Limpia el dato seleccionado o todo el contenido de la lista."""
    seleccion = lista.curselection()
    if seleccion:  # Si hay un elemento seleccionado
        lista.delete(seleccion)
    else:  # Si no hay selección, limpiar toda la lista
        lista.delete(0, tk.END)

# -------------------------------
# Ventana principal
# -------------------------------
ventana = tk.Tk()
ventana.title("Aplicación GUI Básica - Gestión de Datos")
ventana.geometry("400x300")

# -------------------------------
# Componentes GUI
# -------------------------------
# Etiqueta
label = tk.Label(ventana, text="Ingresa un dato:")
label.pack(pady=5)

# Campo de texto
entrada = tk.Entry(ventana, width=40)
entrada.pack(pady=5)

# Botón Agregar
btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato)
btn_agregar.pack(pady=5)

# Botón Limpiar
btn_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_dato)
btn_limpiar.pack(pady=5)

# Lista para mostrar datos
lista = tk.Listbox(ventana, width=50, height=10)
lista.pack(pady=10)

# -------------------------------
# Ejecutar aplicación
# -------------------------------
ventana.mainloop()
