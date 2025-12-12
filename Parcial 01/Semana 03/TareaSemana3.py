# Programa Orientado a Objetos para calcular el promedio semanal del clima

class ClimaDiario:
    """
    Clase que representa la información diaria del clima.
    """
    def __init__(self, temperatura):
        # Encapsulamiento: atributo privado
        self.__temperatura = temperatura

    def obtener_temperatura(self):
        """
        Método getter para acceder a la temperatura.
        """
        return self.__temperatura


class ClimaSemanal:
    """
    Clase que representa el conjunto de temperaturas de la semana.
    """
    def __init__(self):
        self.dias = []  # Lista de objetos ClimaDiario

    def ingresar_temperaturas(self):
        """
        Método para ingresar las temperaturas de los 7 días.
        """
        for dia in range(1, 8):
            temp = float(input(f"Ingrese la temperatura del día {dia}: "))
            self.dias.append(ClimaDiario(temp))

    def calcular_promedio(self):
        """
        Método para calcular el promedio semanal usando polimorfismo (acceso a método getter).
        """
        total = sum([dia.obtener_temperatura() for dia in self.dias])
        return total / len(self.dias)


def main():
    """
    Método principal que organiza el flujo del programa.
    """
    print("=== Promedio Semanal del Clima (POO) ===")
    semana = ClimaSemanal()
    semana.ingresar_temperaturas()
    promedio = semana.calcular_promedio()
    print(f"El promedio semanal de temperatura es: {promedio:.2f} °C")

# Ejecutar el programa
if __name__ == "__main__":
    main()