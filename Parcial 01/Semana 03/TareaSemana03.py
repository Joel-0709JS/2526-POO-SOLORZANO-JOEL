# Programa Tradicional para calcular el promedio semanal del clima

def ingresar_temperaturas():
    """
    Función para ingresar las temperaturas diarias de la semana.
    Retorna una lista con las 7 temperaturas ingresadas.
    """
    temperaturas = []
    for dia in range(1, 8):  # 7 días de la semana
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """
    Función que recibe una lista de temperaturas y calcula el promedio semanal.
    """
    return sum(temperaturas) / len(temperaturas)

def main():
    """
    Función principal que organiza el flujo del programa.
    """
    print("=== Promedio Semanal del Clima (Programación Tradicional) ===")
    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    print(f"El promedio semanal de temperatura es: {promedio:.2f} °C")

# Ejecutar el programa
if __name__ == "__main__":
    main()