import json
import os


# ==============================================================================
# CLASE PRODUCTO
# ==============================================================================
class Producto:
    """
    Representa un ítem individual en el inventario.
    Encapsula los datos del producto y valida su integridad.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters y Setters con validación básica (Encapsulamiento)
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor:
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = int(valor)

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = float(valor)

    def to_dict(self):
        """Convierte el objeto a un diccionario para serialización JSON."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un objeto Producto desde un diccionario (Deserialización)."""
        return cls(
            id_producto=datos["id"],
            nombre=datos["nombre"],
            cantidad=datos["cantidad"],
            precio=datos["precio"]
        )

    def __str__(self):
        return f"ID: {self._id} | {self._nombre} | Cant: {self._cantidad} | Precio: ${self._precio:.2f}"


# ==============================================================================
# CLASE INVENTARIO
# ==============================================================================
class Inventario:
    """
    Gestiona la colección de productos.
    Utiliza un diccionario para acceso rápido por ID (O(1)).
    Maneja la persistencia de datos en archivos JSON.
    """

    def __init__(self, archivo_guardado="inventario.json"):
        self.archivo_guardado = archivo_guardado
        # Usamos un DICCIONARIO donde la clave es el ID del producto.
        # Esto optimiza la búsqueda, eliminación y actualización a O(1).
        self.productos = {}
        self.cargar()

    def cargar(self):
        """Lee el archivo JSON y reconstruye el inventario en memoria."""
        if os.path.exists(self.archivo_guardado):
            try:
                with open(self.archivo_guardado, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    # Convertimos cada diccionario de la lista en un objeto Producto
                    for item in datos:
                        producto = Producto.from_dict(item)
                        self.productos[producto.id] = producto
                print(f"Inventario cargado exitosamente desde {self.archivo_guardado}.")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error al cargar el archivo: {e}. Iniciando inventario vacío.")
                self.productos = {}
        else:
            print("No se encontró archivo previo. Iniciando inventario nuevo.")

    def guardar(self):
        """Serializa el inventario actual y lo escribe en el archivo JSON."""
        try:
            # Convertimos la colección de objetos a una lista de diccionarios
            lista_datos = [p.to_dict() for p in self.productos.values()]
            with open(self.archivo_guardado, "w", encoding="utf-8") as f:
                json.dump(lista_datos, f, indent=4, ensure_ascii=False)
            print("Inventario guardado correctamente.")
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    def agregar_producto(self, producto):
        """Añade un nuevo producto si el ID no existe."""
        if producto.id in self.productos:
            print(f"Error: El producto con ID {producto.id} ya existe.")
            return False
        self.productos[producto.id] = producto
        self.guardar()
        print(f"Producto '{producto.nombre}' añadido correctamente.")
        return True

    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID único."""
        if id_producto in self.productos:
            eliminado = self.productos.pop(id_producto)
            self.guardar()
            print(f"Producto '{eliminado.nombre}' eliminado.")
            return True
        else:
            print(f"Error: No se encontró el producto con ID {id_producto}.")
            return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualiza cantidad o precio de un producto existente."""
        if id_producto in self.productos:
            prod = self.productos[id_producto]
            if cantidad is not None:
                prod.cantidad = cantidad
            if precio is not None:
                prod.precio = precio
            self.guardar()
            print(f"Producto '{prod.nombre}' actualizado.")
            return True
        else:
            print(f"Error: No se encontró el producto con ID {id_producto}.")
            return False

    def buscar_por_nombre(self, nombre_busqueda):
        """
        Busca productos por nombre.
        Utiliza una LISTA por comprensión para filtrar los valores del diccionario.
        La búsqueda es insensible a mayúsculas/minúsculas.
        """
        resultados = [p for p in self.productos.values() if nombre_busqueda.lower() in p.nombre.lower()]
        return resultados

    def mostrar_todos(self):
        """Retorna una lista con todos los productos actuales."""
        return list(self.productos.values())


# ==============================================================================
# INTERFAZ DE USUARIO (MAIN)
# ==============================================================================
def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO ===")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar producto (Cantidad/Precio)")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todo el inventario")
    print("6. Salir")
    return input("Seleccione una opción: ")


def obtener_entero(mensaje):
    """Helper para validar entrada numérica."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Por favor, ingrese un número válido.")


def obtener_float(mensaje):
    """Helper para validar entrada decimal."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor, ingrese un número válido.")


def main():
    sistema = Inventario()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":  # Añadir
            print("\n--- Añadir Producto ---")
            try:
                id_p = obtener_entero("ID del producto (único): ")
                nombre = input("Nombre del producto: ")
                cant = obtener_entero("Cantidad inicial: ")
                prec = obtener_float("Precio unitario: ")

                nuevo_prod = Producto(id_p, nombre, cant, prec)
                sistema.agregar_producto(nuevo_prod)
            except ValueError as e:
                print(f"Error de validación: {e}")

        elif opcion == "2":  # Eliminar
            print("\n--- Eliminar Producto ---")
            id_p = obtener_entero("ID del producto a eliminar: ")
            sistema.eliminar_producto(id_p)

        elif opcion == "3":  # Actualizar
            print("\n--- Actualizar Producto ---")
            id_p = obtener_entero("ID del producto a actualizar: ")
            print("Deje en blanco (presione Enter) si no desea cambiar un campo.")

            cant_input = input("Nueva cantidad (Enter para omitir): ")
            prec_input = input("Nuevo precio (Enter para omitir): ")

            nueva_cant = int(cant_input) if cant_input else None
            nuevo_prec = float(prec_input) if prec_input else None

            sistema.actualizar_producto(id_p, nueva_cant, nuevo_prec)

        elif opcion == "4":  # Buscar
            print("\n--- Buscar Producto ---")
            nombre = input("Ingrese nombre o parte del nombre: ")
            resultados = sistema.buscar_por_nombre(nombre)
            if resultados:
                print(f"\nSe encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos con ese nombre.")

        elif opcion == "5":  # Mostrar Todos
            print("\n--- Inventario Completo ---")
            todos = sistema.mostrar_todos()
            if todos:
                for p in todos:
                    print(p)
                print(f"\nTotal de ítems únicos: {len(todos)}")
            else:
                print("El inventario está vacío.")

        elif opcion == "6":  # Salir
            print("Guardando cambios antes de salir...")
            sistema.guardar()
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()