"""
Sistema de Gestión de Inventarios - Versión Simple y Funcional
"""


class Producto:
    """Representa un producto en el inventario."""

    def __init__(self, id_producto, nombre, cantidad, precio):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")

        self._id_producto = id_producto
        self._nombre = nombre.strip()
        self._cantidad = cantidad
        self._precio = round(precio, 2)

    @property
    def id_producto(self):
        return self._id_producto

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        self._nombre = nuevo_nombre.strip()

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = nueva_cantidad

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = round(nuevo_precio, 2)

    def __str__(self):
        return (f"ID: {self._id_producto:4d} | "
                f"Nombre: {self._nombre:<20} | "
                f"Cantidad: {self._cantidad:4d} | "
                f"Precio: ${self._precio:7.2f}")


class Inventario:
    """Gestiona una colección de productos."""

    def __init__(self):
        self._productos = []

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("El objeto debe ser una instancia de Producto")

        if self._buscar_por_id(producto.id_producto):
            print(f"ERROR: Ya existe un producto con ID {producto.id_producto}")
            return False

        self._productos.append(producto)
        print(f"Producto '{producto.nombre}' agregado exitosamente")
        return True

    def eliminar_producto(self, id_producto):
        producto = self._buscar_por_id(id_producto)
        if producto:
            self._productos.remove(producto)
            print(f"Producto '{producto.nombre}' (ID: {id_producto}) eliminado")
            return True
        else:
            print(f"ERROR: No se encontro producto con ID {id_producto}")
            return False

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        producto = self._buscar_por_id(id_producto)
        if not producto:
            print(f"ERROR: No se encontro producto con ID {id_producto}")
            return False

        cambios = []
        if nueva_cantidad is not None:
            producto.cantidad = nueva_cantidad
            cambios.append(f"cantidad a {nueva_cantidad}")

        if nuevo_precio is not None:
            producto.precio = nuevo_precio
            cambios.append(f"precio a ${nuevo_precio:.2f}")

        if cambios:
            print(f"Producto '{producto.nombre}' actualizado: {', '.join(cambios)}")
            return True
        else:
            print("No se especificaron cambios para actualizar")
            return False

    def buscar_por_nombre(self, nombre_busqueda):
        nombre_busqueda = nombre_busqueda.strip().lower()
        if not nombre_busqueda:
            return self._productos[:]

        return [
            producto for producto in self._productos
            if nombre_busqueda in producto.nombre.lower()
        ]

    def mostrar_inventario(self):
        if not self._productos:
            print("\nEl inventario esta vacío")
            return

        print("\n" + "=" * 70)
        print("INVENTARIO ACTUAL".center(70))
        print("=" * 70)
        print(f"{'ID':<6} | {'NOMBRE':<20} | {'CANTIDAD':<10} | {'PRECIO':<12}")
        print("-" * 70)

        for producto in sorted(self._productos, key=lambda p: p.id_producto):
            print(f"{producto.id_producto:<6} | {producto.nombre:<20} | "
                  f"{producto.cantidad:<10} | ${producto.precio:<11.2f}")

        print("=" * 70)
        print(f"Total de productos: {len(self._productos)}")
        print("=" * 70 + "\n")

    def _buscar_por_id(self, id_producto):
        for producto in self._productos:
            if producto.id_producto == id_producto:
                return producto
        return None

    @property
    def cantidad_productos(self):
        return len(self._productos)


def mostrar_menu():
    print("\n" + "=" * 60)
    print("GESTION DE INVENTARIOS - TIENDA".center(60))
    print("=" * 60)
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar producto (cantidad/precio)")
    print("4. Buscar producto por nombre")
    print("5. Mostrar todos los productos")
    print("0. Salir del sistema")
    print("=" * 60)


def solicitar_entero(mensaje, min_valor=None, max_valor=None):
    while True:
        try:
            valor = int(input(mensaje))
            if min_valor is not None and valor < min_valor:
                print(f"El valor debe ser mayor o igual a {min_valor}")
                continue
            if max_valor is not None and valor > max_valor:
                print(f"El valor debe ser menor o igual a {max_valor}")
                continue
            return valor
        except ValueError:
            print("ERROR: Debe ingresar un numero entero valido")
        except KeyboardInterrupt:
            print("\nOperacion cancelada por el usuario")
            exit(0)


def solicitar_float(mensaje, min_valor=None):
    while True:
        try:
            valor = float(input(mensaje))
            if min_valor is not None and valor < min_valor:
                print(f"El valor debe ser mayor o igual a {min_valor}")
                continue
            return valor
        except ValueError:
            print("ERROR: Debe ingresar un numero valido")
        except KeyboardInterrupt:
            print("\nOperacion cancelada por el usuario")
            exit(0)


def agregar_producto(inventario):
    print("\n--- AÑADIR NUEVO PRODUCTO ---")

    id_producto = solicitar_entero("Ingrese ID del producto: ", min_valor=1)

    if inventario._buscar_por_id(id_producto):
        print(f"ERROR: Ya existe un producto con ID {id_producto}")
        return

    nombre = input("Ingrese nombre del producto: ").strip()
    while not nombre:
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese nombre del producto: ").strip()

    cantidad = solicitar_entero("Ingrese cantidad inicial: ", min_valor=0)
    precio = solicitar_float("Ingrese precio unitario: $", min_valor=0.0)

    producto = Producto(id_producto, nombre, cantidad, precio)
    inventario.agregar_producto(producto)


def eliminar_producto(inventario):
    print("\n--- ELIMINAR PRODUCTO ---")
    if inventario.cantidad_productos == 0:
        print("El inventario esta vacío. No hay productos para eliminar.")
        return

    id_producto = solicitar_entero("Ingrese ID del producto a eliminar: ", min_valor=1)
    inventario.eliminar_producto(id_producto)


def actualizar_producto(inventario):
    print("\n--- ACTUALIZAR PRODUCTO ---")
    if inventario.cantidad_productos == 0:
        print("El inventario esta vacío. No hay productos para actualizar.")
        return

    id_producto = solicitar_entero("Ingrese ID del producto a actualizar: ", min_valor=1)

    print("\nQue desea actualizar?")
    print("1. Cantidad")
    print("2. Precio")
    print("3. Ambos")

    opcion = solicitar_entero("Seleccione una opción (1-3): ", min_valor=1, max_valor=3)

    nueva_cantidad = None
    nuevo_precio = None

    if opcion in [1, 3]:
        nueva_cantidad = solicitar_entero("Nueva cantidad: ", min_valor=0)
    if opcion in [2, 3]:
        nuevo_precio = solicitar_float("Nuevo precio: $", min_valor=0.0)

    inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio)


def buscar_producto(inventario):
    print("\n--- BUSCAR PRODUCTO POR NOMBRE ---")
    if inventario.cantidad_productos == 0:
        print("El inventario esta vacío.")
        return

    nombre_busqueda = input("Ingrese nombre o parte del nombre a buscar: ").strip()

    resultados = inventario.buscar_por_nombre(nombre_busqueda)

    if not resultados:
        print(f"No se encontraron productos que contengan '{nombre_busqueda}'")
        return

    print(f"\nSe encontraron {len(resultados)} resultado(s):")
    print("-" * 70)
    for producto in resultados:
        print(producto)
    print("-" * 70)


def main():
    inventario = Inventario()

    print("=" * 60)
    print("SISTEMA DE GESTION DE INVENTARIOS".center(60))
    print("=" * 60)

    # Opción para cargar datos de ejemplo
    print("\nDesea cargar datos de ejemplo para pruebas? (s/n)")
    if input("> ").strip().lower() in ['s', 'si', 'sí']:
        productos_ejemplo = [
            Producto(1, "Laptop Dell", 10, 799.99),
            Producto(2, "Mouse Logitech", 50, 25.50),
            Producto(3, "Teclado Mecánico", 30, 89.99),
            Producto(4, "Monitor 24", 15, 199.99),
            Producto(5, "USB 64GB", 100, 15.99)
        ]
        for p in productos_ejemplo:
            inventario.agregar_producto(p)
        print("Datos de ejemplo cargados exitosamente")

    while True:
        try:
            mostrar_menu()
            opcion = solicitar_entero("Seleccione una opción (0-5): ", min_valor=0, max_valor=5)

            if opcion == 0:
                print("\nGracias por usar el sistema de gestion de inventarios!")
                print("Saliendo del sistema...")
                break
            elif opcion == 1:
                agregar_producto(inventario)
            elif opcion == 2:
                eliminar_producto(inventario)
            elif opcion == 3:
                actualizar_producto(inventario)
            elif opcion == 4:
                buscar_producto(inventario)
            elif opcion == 5:
                inventario.mostrar_inventario()

            if opcion != 0:
                input("\nPresione Enter para continuar...")

        except KeyboardInterrupt:
            print("\nOperacion cancelada por el usuario")
            break
        except Exception as e:
            print(f"\nERROR inesperado: {type(e).__name__} - {e}")
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
