class Persona:
    def __init__(self, nombre, edad):
        """
        Constructor: se ejecuta al crear el objeto.
        """
        self.nombre = nombre
        self.edad = edad
        print(f" Constructor: Se ha creado la persona {self.nombre}, edad {self.edad}.")

    def saludar(self):
        """
        Método normal de la clase.
        """
        print(f" Hola, mi nombre es {self.nombre} y tengo {self.edad} años.")

    def __del__(self):
        """
        Destructor: se ejecuta al eliminar el objeto o al finalizar el programa.
        """
        print(f" Destructor: La persona {self.nombre} ha sido eliminada de la memoria.")

# Programa principal
if __name__ == "__main__":
    persona1 = Persona("Joel Solorzano", 31)   # Mensaje del constructor
    persona1.saludar()               # Mensaje del método normal

    # Eliminamos el objeto explícitamente
    del persona1                     # Mensaje del destructor
