# Conversor_temperatura.py
# Este programa convierte temperaturas entre grados Celsius y Fahrenheit.
# El usuario elige la dirección de la conversión e ingresa el valor a convertir.

def celsius_a_fahrenheit(celsius):
    """
    Convierte una temperatura en grados Celsius a Fahrenheit.
    :param celsius: Temperatura en grados Celsius (float)
    :return: Temperatura equivalente en grados Fahrenheit (float)
    """
    fahrenheit = (celsius * 9 / 5) + 32
    return fahrenheit


def fahrenheit_a_celsius(fahrenheit):
    """
    Convierte una temperatura en grados Fahrenheit a Celsius.
    :param fahrenheit: Temperatura en grados Fahrenheit (float)
    :return: Temperatura equivalente en grados Celsius (float)
    """
    celsius = (fahrenheit - 32) * 5 / 9
    return celsius


def main():
    # Mensaje de bienvenida
    print("Bienvenido al Conversor de Temperaturas")

    # Variable booleana para controlar el ciclo
    continuar = True

    while continuar:
        # Mostrar opciones al usuario
        print("\nOpciones:")
        print("1. Convertir de Celsius a Fahrenheit")
        print("2. Convertir de Fahrenheit a Celsius")
        print("3. Salir")

        # Leer la opción del usuario (string inicialmente, luego convertida a int)
        opcion = input("Elige una opción (1, 2 o 3): ")

        # Validar la entrada
        if opcion == "1":
            # Solicitar temperatura en Celsius
            temp_celsius_str = input("Ingresa la temperatura en grados Celsius: ")
            try:
                temp_celsius = float(temp_celsius_str)  # Conversión a float
                resultado = celsius_a_fahrenheit(temp_celsius)
                print(f"{temp_celsius} °C equivalen a {resultado:.2f} °F")
            except ValueError:
                print("Error: Por favor ingresa un número válido.")

        elif opcion == "2":
            # Solicitar temperatura en Fahrenheit
            temp_fahrenheit_str = input("Ingresa la temperatura en grados Fahrenheit: ")
            try:
                temp_fahrenheit = float(temp_fahrenheit_str)  # Conversión a float
                resultado = fahrenheit_a_celsius(temp_fahrenheit)
                print(f"{temp_fahrenheit} °F equivalen a {resultado:.2f} °C")
            except ValueError:
                print("Error: Por favor ingresa un número válido.")

        elif opcion == "3":
            continuar = False  # Cambiar la variable booleana para salir del bucle
            print("¡Gracias por usar el conversor!")

        else:
            print("Opción no válida. Por favor, elige 1, 2 o 3.")


# Ejecutar el programa
if __name__ == "__main__":
    main()