# ============================================
# Ejemplo de Aplicación de Conceptos de POO en Python
# Autor: Joel Aquiles Solorzano Romero
# ============================================

# -------------------------------
# Clase Base: Persona
# -------------------------------
class Persona:
    def __init__(self, nombre, edad):
        # Atributos públicos
        self.nombre = nombre
        self.edad = edad

    def mostrar_info(self):
        """Método que muestra la información básica de la persona"""
        return f"Nombre: {self.nombre}, Edad: {self.edad}"

    def hablar(self):
        """Ejemplo de polimorfismo: este método será sobrescrito en clases derivadas"""
        return f"{self.nombre} está hablando."


# -------------------------------
# Clase Derivada: Estudiante (Herencia)
# -------------------------------
class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        # Llamada al constructor de la clase base
        super().__init__(nombre, edad)
        self.carrera = carrera
        # Atributo encapsulado (privado)
        self.__promedio = None

    # Encapsulación: métodos getter y setter para el atributo privado
    def set_promedio(self, promedio):
        """Setter: asigna un valor al atributo privado __promedio"""
        if 0 <= promedio <= 10:
            self.__promedio = promedio
        else:
            print("Error: El promedio debe estar entre 0 y 10.")

    def get_promedio(self):
        """Getter: devuelve el valor del atributo privado __promedio"""
        return self.__promedio

    # Polimorfismo: sobrescribimos el método hablar
    def hablar(self):
        return f"{self.nombre} (Estudiante de {self.carrera}) está respondiendo en clase."


# -------------------------------
# Clase Derivada: Profesor (Herencia y Polimorfismo)
# -------------------------------
class Profesor(Persona):
    def __init__(self, nombre, edad, materia):
        super().__init__(nombre, edad)
        self.materia = materia

    def hablar(self):
        """Sobrescribimos el método hablar para demostrar polimorfismo"""
        return f"El profesor {self.nombre} está explicando {self.materia}."


# -------------------------------
# Programa Principal
# -------------------------------
if __name__ == "__main__":
    # Crear objetos (instancias)
    persona1 = Persona("Juan Carlos", 34)
    estudiante1 = Estudiante("Linda", 25, "Tecnologías de la Información")
    profesor1 = Profesor("Adrián", 45, "Programación en Python")

    # Uso de métodos
    print(persona1.mostrar_info())
    print(persona1.hablar())

    print(estudiante1.mostrar_info())
    estudiante1.set_promedio(9.5)  # Encapsulación: asignar promedio
    print(f"Promedio de {estudiante1.nombre}: {estudiante1.get_promedio()}")
    print(estudiante1.hablar())  # Polimorfismo

    print(profesor1.mostrar_info())
    print(profesor1.hablar())  # Polimorfismo
