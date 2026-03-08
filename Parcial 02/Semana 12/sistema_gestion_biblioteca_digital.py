# =================================================================
# Tarea: Sistema de Gestión de Biblioteca Digital
# Autor: Joel Solorzano
# =================================================================

class Libro:
    """Representa un libro con atributos inmutables y categorías."""

    def __init__(self, titulo, autor, categoria, isbn):
        # El requisito pide usar una tupla para autor y título (inmutables)
        self.datos_base = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"'{self.datos_base[0]}' | Autor: {self.datos_base[1]} | ISBN: {self.isbn} ({self.categoria})"


class Usuario:
    """Representa a un usuario y su historial de préstamos."""

    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        # Lista para gestionar los libros prestados dinámicamente
        self.libros_prestados = []

    def __str__(self):
        libros_nombres = [libro.datos_base[0] for libro in self.libros_prestados]
        return f"Usuario: {self.nombre} (ID: {self.user_id}) | Libros: {libros_nombres if libros_nombres else 'Ninguno'}"


class Biblioteca:
    """Gestor principal de la colección, usuarios y préstamos."""

    def __init__(self):
        # Diccionario para búsquedas eficientes O(1) usando ISBN como clave
        self.catalogo = {}
        # Conjunto para asegurar IDs únicos de usuarios
        self.usuarios_ids = set()
        # Diccionario para mapear IDs con objetos Usuario
        self.usuarios_registrados = {}

    # --- Gestión de Libros ---
    def añadir_libro(self, libro):
        if libro.isbn not in self.catalogo:
            self.catalogo[libro.isbn] = libro
            print(f"[CATÁLOGO] Libro añadido: {libro.datos_base[0]}")
        else:
            print(f"[ERROR] El ISBN {libro.isbn} ya existe.")

    def quitar_libro(self, isbn):
        if isbn in self.catalogo:
            eliminado = self.catalogo.pop(isbn)
            print(f"[CATÁLOGO] Libro eliminado: {eliminado.datos_base[0]}")
        else:
            print("[ERROR] No se puede eliminar: ISBN no encontrado.")

    # --- Gestión de Usuarios ---
    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.usuarios_ids:
            self.usuarios_ids.add(usuario.user_id)
            self.usuarios_registrados[usuario.user_id] = usuario
            print(f"[REGISTRO] Usuario '{usuario.nombre}' creado exitosamente.")
        else:
            print(f"[ERROR] El ID {usuario.user_id} ya pertenece a otro usuario.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.usuarios_registrados:
            user = self.usuarios_registrados[user_id]
            if not user.libros_prestados:
                self.usuarios_ids.remove(user_id)
                del self.usuarios_registrados[user_id]
                print(f"[REGISTRO] Usuario {user_id} eliminado.")
            else:
                print(f"[AVISO] No se puede dar de baja a {user.nombre}: tiene libros pendientes.")
        else:
            print("[ERROR] Usuario no encontrado.")

    # --- Operaciones de Préstamo ---
    def prestar_libro(self, isbn, user_id):
        if isbn in self.catalogo and user_id in self.usuarios_registrados:
            libro = self.catalogo.pop(isbn)
            usuario = self.usuarios_registrados[user_id]
            usuario.libros_prestados.append(libro)
            print(f"[PRÉSTAMO] '{libro.datos_base[0]}' entregado a {usuario.nombre}.")
        else:
            print("[ERROR] Préstamo fallido: Verifique disponibilidad de libro o ID de usuario.")

    def devolver_libro(self, isbn, user_id):
        if user_id in self.usuarios_registrados:
            usuario = self.usuarios_registrados[user_id]
            for i, libro in enumerate(usuario.libros_prestados):
                if libro.isbn == isbn:
                    libro_devuelto = usuario.libros_prestados.pop(i)
                    self.catalogo[isbn] = libro_devuelto
                    print(f"[DEVOLUCIÓN] '{libro_devuelto.datos_base[0]}' regresó a la biblioteca.")
                    return
            print("[ERROR] El usuario no tiene este libro.")
        else:
            print("[ERROR] Usuario no registrado.")

    # --- Búsquedas ---
    def buscar_libro(self, busqueda):
        print(f"\n--- Resultados de búsqueda para: '{busqueda}' ---")
        encontrados = [libro for libro in self.catalogo.values() if
                       busqueda.lower() in libro.datos_base[0].lower() or
                       busqueda.lower() in libro.datos_base[1].lower() or
                       busqueda.lower() in libro.categoria.lower()]

        if encontrados:
            for l in encontrados: print(f" -> {l}")
        else:
            print("No se encontraron coincidencias.")


# =================================================================
# Bloque de Pruebas (Ejecución del Sistema)
# =================================================================

if __name__ == "__main__":
    biblioteca = Biblioteca()

    # 1. Poblar la biblioteca
    libros_iniciales = [
        Libro("Cien Años de Soledad", "Gabriel García Márquez", "Realismo Mágico", "ISBN001"),
        Libro("Python Crash Course", "Eric Matthes", "Programación", "ISBN002"),
        Libro("1984", "George Orwell", "Ficción/Distopía", "ISBN003"),
        Libro("Clean Code", "Robert C. Martin", "Programación", "ISBN004")
    ]
    for l in libros_iniciales: biblioteca.añadir_libro(l)

    # 2. Registrar usuarios
    user_joel = Usuario("Joel Solorzano", "U101")
    user_maria = Usuario("Maria Lopez", "U102")
    biblioteca.registrar_usuario(user_joel)
    biblioteca.registrar_usuario(user_maria)

    # 3. Realizar préstamos múltiples
    print("\n--- Realizando Préstamos ---")
    biblioteca.prestar_libro("ISBN002", "U101")  # Joel se lleva Python
    biblioteca.prestar_libro("ISBN004", "U101")  # Joel se lleva Clean Code
    biblioteca.prestar_libro("ISBN001", "U102")  # Maria se lleva Cien Años

    # 4. Mostrar estado de los usuarios
    print(f"\nEstado Joel: {user_joel}")
    print(f"Estado Maria: {user_maria}")

    # 5. Probar búsquedas
    biblioteca.buscar_libro("Programación")
    biblioteca.buscar_libro("Orwell")

    # 6. Devolución y Baja
    print("\n--- Pruebas de Cierre ---")
    biblioteca.devolver_libro("ISBN002", "U101")
    biblioteca.dar_baja_usuario("U101")  # Debería fallar (todavía tiene Clean Code)