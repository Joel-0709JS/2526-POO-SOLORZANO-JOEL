import json
import os


# ==========================================
# Clase: Producto
# ==========================================
class Producto:
    """
    Representa un producto individual en el inventario.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        """Convierte el objeto Producto a un diccionario para serialización JSON."""
        return {
            "id": self.id_producto,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(datos):
        """Crea un objeto Producto desde un diccionario (deserialization)."""
        return Producto(
            datos["id"],
            datos["nombre"],
            datos["cantidad"],
            datos["precio"]

        )

    def __str__(self):
        return f"ID: {self.id_producto} | {self.nombre} | Cant: {self.cantidad} | Precio: ${self.precio:.2f}"


# ==========================================
# Clase: Inventario
# ==========================================
class Inventario:
    """
    Gestiona la colección de productos y la persistencia en archivo.
    Implementa manejo de excepciones para operaciones de archivo.
    """

    def __init__(self, archivo_nombre='inventario.txt'):
        self.archivo_nombre = archivo_nombre
        self.productos = []
        self._cargar_inventario()

    def _cargar_inventario(self):
        """
        Carga los productos desde el archivo de texto al iniciar.
        Maneja FileNotFoundError, PermissionError y JSONDecodeError.
        """
        if not os.path.exists(self.archivo_nombre):
            print(f"[INFO] No se encontró '{self.archivo_nombre}'. Se iniciará un inventario vacío.")
            return

        try:
            with open(self.archivo_nombre, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.productos = [Producto.from_dict(p) for p in datos]
                print(
                    f"[ÉXITO] Inventario cargado correctamente desde '{self.archivo_nombre}'. ({len(self.productos)} productos)")

        except FileNotFoundError:
            # Este caso técnicamente ya se cubre con os.path.exists, pero es buena práctica
            print(f"[ADVERTENCIA] El archivo '{self.archivo_nombre}' no existe. Se creará uno nuevo al guardar.")
        except PermissionError:
            print(
                f"[ERROR CRÍTICO] No tienes permisos para leer '{self.archivo_nombre}'. El programa funcionará en memoria solamente.")
        except json.JSONDecodeError:
            print(
                f"[ERROR] El archivo '{self.archivo_nombre}' está corrupto o tiene formato inválido. Se iniciará un inventario vacío para evitar pérdida de datos.")
        except Exception as e:
            print(f"[ERROR INESPERADO] Ocurrió un error al cargar: {e}")

    def _guardar_inventario(self):
        """
        Guarda el estado actual del inventario en el archivo de texto.
        Se llama después de cada modificación (CRUD).
        """
        try:
            with open(self.archivo_nombre, 'w', encoding='utf-8') as f:
                # Convertimos la lista de objetos a lista de diccionarios
                datos = [p.to_dict() for p in self.productos]
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True, "Guardado exitoso"

        except PermissionError:
            return False, "Error: No tienes permisos de escritura en el disco."
        except OSError as e:
            return False, f"Error de Sistema Operativo al escribir: {e}"
        except Exception as e:
            return False, f"Error inesperado al guardar: {e}"

    def agregar_producto(self, producto):
        """Añade un producto y persiste el cambio."""
        # Validar que el ID no exista
        if any(p.id_producto == producto.id_producto for p in self.productos):
            print("[ERROR] Ya existe un producto con ese ID.")
            return False

        self.productos.append(producto)
        exito, mensaje = self._guardar_inventario()

        if exito:
            print(f"[ÉXITO] Producto '{producto.nombre}' añadido y guardado en archivo.")
            return True
        else:
            print(f"[ADVERTENCIA] Producto añadido en memoria, pero {mensaje}. Los cambios podrían perderse al cerrar.")
            return False

    def eliminar_producto(self, id_producto):
        """Elimina un producto por ID y persiste el cambio."""
        producto_encontrado = None
        for p in self.productos:
            if p.id_producto == id_producto:
                producto_encontrado = p
                break

        if producto_encontrado:
            self.productos.remove(producto_encontrado)
            exito, mensaje = self._guardar_inventario()

            if exito:
                print(f"[ÉXITO] Producto ID {id_producto} eliminado y archivo actualizado.")
                return True
            else:
                print(f"[ADVERTENCIA] Producto eliminado en memoria, pero {mensaje}.")
                return False
        else:
            print(f"[ERROR] No se encontró el producto con ID {id_producto}.")
            return False

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """Actualiza campos de un producto y persiste el cambio."""
        for p in self.productos:
            if p.id_producto == id_producto:
                if nueva_cantidad is not None:
                    p.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    p.precio = nuevo_precio

                exito, mensaje = self._guardar_inventario()
                if exito:
                    print(f"[ÉXITO] Producto ID {id_producto} actualizado en archivo.")
                    return True
                else:
                    print(f"[ADVERTENCIA] Producto actualizado en memoria, pero {mensaje}.")
                    return False

        print(f"[ERROR] No se encontró el producto con ID {id_producto} para actualizar.")
        return False

    def mostrar_inventario(self):
        """Muestra todos los productos en consola."""
        if not self.productos:
            print("[INFO] El inventario está vacío.")
        else:
            print("\n--- INVENTARIO ACTUAL ---")
            for p in self.productos:
                print(p)
            print("-------------------------\n")


# ==========================================
# Interfaz de Usuario (Consola)
# ==========================================
def obtener_entero(mensaje):
    """Helper para validar entrada de números enteros."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("[ERROR] Por favor, ingresa un número válido.")


def obtener_flotante(mensaje):
    """Helper para validar entrada de números decimales."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("[ERROR] Por favor, ingresa un número válido.")


def menu():
    print("\n========================================")
    print("   SISTEMA DE GESTIÓN DE INVENTARIOS   ")
    print("========================================")
    inventario = Inventario()  # Al iniciar, carga el archivo automáticamente

    while True:
        print("\n1. Agregar Producto")
        print("2. Eliminar Producto")
        print("3. Actualizar Producto")
        print("4. Mostrar Inventario")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                id_p = obtener_entero("ID del producto: ")
                nombre = input("Nombre del producto: ")
                cant = obtener_entero("Cantidad: ")
                precio = obtener_flotante("Precio: ")

                nuevo_prod = Producto(id_p, nombre, cant, precio)
                inventario.agregar_producto(nuevo_prod)
            except KeyboardInterrupt:
                print("\n[INFO] Operación cancelada por el usuario.")
            except Exception as e:
                print(f"[ERROR] Ocurrió un error inesperado: {e}")

        elif opcion == '2':
            try:
                id_p = obtener_entero("ID del producto a eliminar: ")
                inventario.eliminar_producto(id_p)
            except KeyboardInterrupt:
                print("\n[INFO] Operación cancelada por el usuario.")

        elif opcion == '3':
            try:
                id_p = obtener_entero("ID del producto a actualizar: ")
                print("Deje en blanco si no desea cambiar un campo.")
                cant_input = input("Nueva cantidad (Enter para omitir): ")
                precio_input = input("Nuevo precio (Enter para omitir): ")

                nueva_cant = int(cant_input) if cant_input.strip() else None
                nuevo_precio = float(precio_input) if precio_input.strip() else None

                inventario.actualizar_producto(id_p, nueva_cant, nuevo_precio)
            except ValueError:
                print("[ERROR] Entrada inválida para cantidad o precio.")
            except KeyboardInterrupt:
                print("\n[INFO] Operación cancelada por el usuario.")

        elif opcion == '4':
            inventario.mostrar_inventario()

        elif opcion == '5':
            print("[INFO] Guardando cambios finales y saliendo...")
            # Se guarda explícitamente al salir por seguridad, aunque ya se guarda en cada cambio
            inventario._guardar_inventario()
            print("¡Hasta luego!")
            break
        else:
            print("[ERROR] Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        # Captura de seguridad a nivel global
        print(f"\n[ERROR CRÍTICO DEL SISTEMA] El programa se cerró inesperadamente: {e}")
