"""
Ejemplo del Mundo Real: Sistema de Tienda de Ropa
Objetivo: Modelar una tienda de ropa utilizando POO en Python.
"""


class Producto:
    """Clase base para representar un producto en la tienda."""

    def __init__(self, nombre, precio, stock):
        self.__nombre = nombre  # Encapsulamiento: atributos privados
        self.__precio = precio
        self.__stock = stock

    # Getters
    def get_nombre(self):
        return self.__nombre

    def get_precio(self):
        return self.__precio

    def get_stock(self):
        return self.__stock

    # Setters
    def set_stock(self, nuevo_stock):
        if nuevo_stock >= 0:
            self.__stock = nuevo_stock
        else:
            print("El stock no puede ser negativo.")

    def mostrar_info(self):
        """Método para mostrar información del producto."""
        return f"{self.__nombre} - ${self.__precio:.2f} - Stock: {self.__stock}"

    def vender(self, cantidad):
        """Método para vender una cantidad del producto."""
        if cantidad <= self.__stock:
            self.__stock -= cantidad
            return True
        else:
            print(f"No hay suficiente stock de {self.__nombre}.")
            return False


class Camisa(Producto):
    """Clase derivada de Producto para camisas."""

    def __init__(self, nombre, precio, stock, talla, color):
        super().__init__(nombre, precio, stock)
        self.__talla = talla
        self.__color = color

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} | Talla: {self.__talla}, Color: {self.__color}"


class Pantalon(Producto):
    """Clase derivada de Producto para pantalones."""

    def __init__(self, nombre, precio, stock, talla, material):
        super().__init__(nombre, precio, stock)
        self.__talla = talla
        self.__material = material

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} | Talla: {self.__talla}, Material: {self.__material}"


class Zapato(Producto):
    """Clase derivada de Producto para zapatos."""

    def __init__(self, nombre, precio, stock, numero, tipo):
        super().__init__(nombre, precio, stock)
        self.__numero = numero
        self.__tipo = tipo  # ej: "deportivo", "formal"

    def mostrar_info(self):
        info_base = super().mostrar_info()
        return f"{info_base} | Número: {self.__numero}, Tipo: {self.__tipo}"


class Cliente:
    """Clase que representa a un cliente de la tienda."""

    def __init__(self, nombre, email):
        self.__nombre = nombre
        self.__email = email
        self.__carrito = []  # Lista de productos comprados

    def agregar_al_carrito(self, producto, cantidad):
        """Agrega un producto al carrito si hay stock disponible."""
        if producto.vender(cantidad):
            self.__carrito.append((producto, cantidad))
            print(f"{cantidad}x {producto.get_nombre()} agregado(s) al carrito.")
        else:
            print(f"No se pudo agregar {producto.get_nombre()} al carrito.")

    def ver_carrito(self):
        """Muestra el contenido del carrito."""
        if not self.__carrito:
            print("El carrito está vacío.")
            return

        print("\n--- Carrito de Compras ---")
        total = 0
        for producto, cantidad in self.__carrito:
            subtotal = producto.get_precio() * cantidad
            total += subtotal
            print(f"{cantidad}x {producto.get_nombre()} - ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")

    def finalizar_compra(self):
        """Finaliza la compra y limpia el carrito."""
        if not self.__carrito:
            print("No hay nada en el carrito para comprar.")
            return

        print("\n Compra finalizada con éxito!")
        self.ver_carrito()
        self.__carrito.clear()
        print("El carrito ha sido vaciado.\n")


class Tienda:
    """Clase que gestiona la tienda y sus productos."""

    def __init__(self, nombre):
        self.__nombre = nombre
        self.__productos = []

    def agregar_producto(self, producto):
        """Agrega un producto al inventario de la tienda."""
        self.__productos.append(producto)
        print(f"Producto '{producto.get_nombre()}' agregado al inventario.")

    def mostrar_inventario(self):
        """Muestra todos los productos disponibles en la tienda."""
        print(f"\n--- Inventario de {self.__nombre} ---")
        if not self.__productos:
            print("No hay productos en el inventario.")
            return

        for i, producto in enumerate(self.__productos, 1):
            print(f"{i}. {producto.mostrar_info()}")

    def buscar_producto_por_nombre(self, nombre):
        """Busca un producto por su nombre."""
        for producto in self.__productos:
            if producto.get_nombre().lower() == nombre.lower():
                return producto
        return None


# --- Ejemplo de uso ---
if __name__ == "__main__":
    print(" Bienvenidos a la Tienda de Ropa 'Joel J.S Express'!\n")

    # Crear la tienda
    tienda = Tienda("ModaExpress")

    # Crear productos
    camisa1 = Camisa("Camisa Azul", 25.99, 10, "M", "Azul")
    pantalon1 = Pantalon("Jeans Negro", 45.50, 5, "32", "Denim")
    zapato1 = Zapato("Zapatillas Nike", 89.99, 8, 42, "Deportivo")

    # Agregar productos a la tienda
    tienda.agregar_producto(camisa1)
    tienda.agregar_producto(pantalon1)
    tienda.agregar_producto(zapato1)

    # Mostrar inventario
    tienda.mostrar_inventario()

    # Crear cliente
    cliente = Cliente("Ana López", "ana@example.com")

    # Simular compra
    print("\n🛒 Cliente realiza compras:")
    producto_buscado = tienda.buscar_producto_por_nombre("Camisa Azul")
    if producto_buscado:
        cliente.agregar_al_carrito(producto_buscado, 2)

    producto_buscado = tienda.buscar_producto_por_nombre("Jeans Negro")
    if producto_buscado:
        cliente.agregar_al_carrito(producto_buscado, 1)

    # Ver carrito
    cliente.ver_carrito()

    # Finalizar compra
    cliente.finalizar_compra()

    # Mostrar inventario actualizado
    print("\n Inventario después de la compra:")
    tienda.mostrar_inventario()