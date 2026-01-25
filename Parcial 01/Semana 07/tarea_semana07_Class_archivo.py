import os
import tempfile

class ArchivoTemporal:
    """
    Clase que representa un archivo temporal.
    - El constructor (__init__) crea un archivo temporal vacío.
    - El destructor (__del__) elimina el archivo cuando el objeto es destruido.
    """

    def __init__(self, contenido=""):
        """
        Constructor de la clase.
        Crea un archivo temporal y escribe contenido opcional en él.
        :param contenido: (str) Contenido inicial del archivo.
        """
        # Crear un archivo temporal único
        fd, self.ruta = tempfile.mkstemp(suffix='.tmp', prefix='temp_')
        os.close(fd)  # Cerramos el descriptor de archivo inmediatamente

        # Escribir contenido si se proporciona
        if contenido:
            with open(self.ruta, 'w') as f:
                f.write(contenido)

        print(f"[INFO] Archivo temporal creado: {self.ruta}")

    def __del__(self):
        """
        Destructor de la clase.
        Elimina el archivo temporal del sistema de archivos si aún existe.
        Se activa cuando el objeto es destruido por el recolector de basura.
        """
        if hasattr(self, 'ruta') and os.path.exists(self.ruta):
            os.remove(self.ruta)
            print(f"[INFO] Archivo temporal eliminado: {self.ruta}")
        else:
            print("[INFO] No hay archivo para eliminar o ya fue borrado.")

    def obtener_ruta(self):
        """Devuelve la ruta del archivo temporal."""
        return self.ruta

    def leer_contenido(self):
        """Lee y devuelve el contenido del archivo."""
        if os.path.exists(self.ruta):
            with open(self.ruta, 'r') as f:
                return f.read()
        return ""

# === Ejemplo de uso ===
if __name__ == "__main__":
    print("=== Creando objeto ArchivoTemporal ===")
    archivo = ArchivoTemporal("Hola, este es un archivo temporal.")
    print(f"Ruta: {archivo.obtener_ruta()}")
    print(f"Contenido: {archivo.leer_contenido()}")

    print("\n=== Simulando finalización del programa ===")
    # El destructor se llamará automáticamente cuando 'archivo' salga de ámbito
    # o cuando el intérprete termine (dependiendo del GC)
    del archivo  # Forzamos la eliminación (opcional, solo para demostración)