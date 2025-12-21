"""
Ejemplo del Mundo Real: Sistema de Reservas de Mesas en un Restaurante
Objetivo: Aplicar POO para modelar mesas, clientes y reservas.
"""


class Mesa:
    """Clase base para representar una mesa en el restaurante."""

    def __init__(self, numero, capacidad):
        self.__numero = numero
        self.__capacidad = capacidad
        self.__disponible = True  # Estado inicial: disponible
        self.__cliente = None  # Quién la tiene reservada

    def get_numero(self):
        return self.__numero

    def get_capacidad(self):
        return self.__capacidad

    def esta_disponible(self):
        return self.__disponible

    def reservar(self, cliente):
        if self.__disponible:
            self.__disponible = False
            self.__cliente = cliente
            print(f" Mesa {self.__numero} reservada para {cliente.get_nombre()}.")
            return True
        else:
            print(f" Mesa {self.__numero} ya está ocupada.")
            return False

    def liberar(self):
        if not self.__disponible:
            self.__disponible = True
            cliente_anterior = self.__cliente
            self.__cliente = None
            print(f" Mesa {self.__numero} liberada. Anterior cliente: {cliente_anterior.get_nombre()}")
            return True
        else:
            print(f" Mesa {self.__numero} ya estaba disponible.")
            return False

    def mostrar_estado(self):
        estado = "Disponible" if self.__disponible else f"Reservada por {self.__cliente.get_nombre()}"
        return f"Mesa {self.__numero} (Capacidad: {self.__capacidad}) - {estado}"


class Cliente:
    """Clase que representa a un cliente del restaurante."""

    def __init__(self, nombre, telefono):
        self.__nombre = nombre
        self.__telefono = telefono
        self.__reserva = None  # Referencia a la mesa reservada

    def get_nombre(self):
        return self.__nombre

    def hacer_reserva(self, mesa):
        if mesa.reservar(self):
            self.__reserva = mesa
            return True
        return False

    def cancelar_reserva(self):
        if self.__reserva:
            mesa = self.__reserva
            mesa.liberar()
            self.__reserva = None
            print(f" {self.__nombre} canceló su reserva.")
            return True
        else:
            print(f" {self.__nombre} no tenía reserva activa.")
            return False

    def info(self):
        if self.__reserva:
            return f"{self.__nombre} ({self.__telefono}) - Reserva en Mesa {self.__reserva.get_numero()}"
        else:
            return f"{self.__nombre} ({self.__telefono}) - Sin reserva"


class Restaurante:
    """Clase que gestiona las mesas y clientes del restaurante."""

    def __init__(self, nombre):
        self.__nombre = nombre
        self.__mesas = []
        self.__clientes = []

    def agregar_mesa(self, numero, capacidad):
        mesa = Mesa(numero, capacidad)
        self.__mesas.append(mesa)
        print(f" Mesa {numero} (capacidad {capacidad}) añadida al restaurante.")
        return mesa

    def registrar_cliente(self, nombre, telefono):
        cliente = Cliente(nombre, telefono)
        self.__clientes.append(cliente)
        print(f" Cliente '{nombre}' registrado.")
        return cliente

    def buscar_mesa_por_numero(self, numero):
        for mesa in self.__mesas:
            if mesa.get_numero() == numero:
                return mesa
        return None

    def mostrar_mesas(self):
        print(f"\n Mesas en {self.__nombre}:")
        for mesa in self.__mesas:
            print(" - " + mesa.mostrar_estado())

    def mostrar_clientes(self):
        print(f"\n Clientes registrados en {self.__nombre}:")
        for cliente in self.__clientes:
            print(" - " + cliente.info())


# --- Ejemplo de uso ---
if __name__ == "__main__":
    print(" Bienvenido al Restaurante 'Colorado J.S'!\n")

    # Crear restaurante
    restaurante = Restaurante("Colorado J.S")

    # Agregar mesas
    mesa1 = restaurante.agregar_mesa(1, 4)
    mesa2 = restaurante.agregar_mesa(2, 2)
    mesa3 = restaurante.agregar_mesa(3, 6)

    # Registrar clientes
    cliente1 = restaurante.registrar_cliente("Ana", "555-1234")
    cliente2 = restaurante.registrar_cliente("Carlos", "555-5678")

    # Mostrar estado inicial
    restaurante.mostrar_mesas()

    # Interacción: Cliente 1 reserva mesa 1
    print("\n Ana intenta reservar:")
    cliente1.hacer_reserva(mesa1)

    # Cliente 2 intenta reservar la misma mesa
    print("\n Carlos intenta reservar:")
    cliente2.hacer_reserva(mesa1)  # Fallará

    # Cliente 2 reservar otra mesa
    cliente2.hacer_reserva(mesa2)

    # Mostrar estado actualizado
    restaurante.mostrar_mesas()

    # Cancelar reserva
    print("\n Ana cancela su reserva:")
    cliente1.cancelar_reserva()

    # Mostrar estado final
    restaurante.mostrar_mesas()