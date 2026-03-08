"""
Sistema de Gestión de Biblioteca Digital
----------------------------------------
Este módulo implementa un sistema básico para gestionar libros, usuarios y préstamos.
Cumple con los requisitos de uso de colecciones específicas de Python:
- Tuplas: Para datos inmutables de los libros.
- Listas: Para gestionar los préstamos de cada usuario.
- Diccionarios: Para acceso rápido a libros por ISBN.
- Conjuntos: Para garantizar unicidad en IDs de usuarios.
"""


class Libro:
    """
    Clase que representa un libro en la biblioteca.
    """

    def __init__(self, titulo, autor, categoria, isbn):
        """
        Inicializa un nuevo libro.

        Args:
            titulo (str): Título del libro.
            autor (str): Autor del libro.
            categoria (str): Categoría o género del libro.
            isbn (str): Identificador único internacional del libro.
        """
        # REQUISITO: Utilizar una tupla para almacenar el autor y el título.
        # Se usa una tupla porque estos datos no deberían cambiar una vez creado el libro.
        self.identidad = (titulo, autor)

        self.categoria = categoria
        self.isbn = isbn

    @property
    def titulo(self):
        """Getter para el título (accediendo a la tupla)."""
        return self.identidad[0]

    @property
    def autor(self):
        """Getter para el autor (accediendo a la tupla)."""
        return self.identidad[1]

    def __str__(self):
        """Representación en cadena del libro para impresión amigable."""
        return f"'{self.titulo}' por {self.autor} (ISBN: {self.isbn})"

    def __repr__(self):
        return f"Libro({self.titulo}, {self.autor}, {self.isbn})"


class Usuario:
    """
    Clase que representa a un usuario registrado en la biblioteca.
    """

    def __init__(self, nombre, id_usuario):
        """
        Inicializa un nuevo usuario.

        Args:
            nombre (str): Nombre completo del usuario.
            id_usuario (str/int): Identificador único del usuario.
        """
        self.nombre = nombre
        self.id_usuario = id_usuario
        # REQUISITO: Utilizar una lista para gestionar los libros prestados.
        # La lista permite mantener un orden y permitir duplicados si la lógica lo permitiera (aquí no).
        self.libros_prestados = []

    def prestar_libro(self, libro):
        """Añade un libro a la lista de préstamos del usuario."""
        self.libros_prestados.append(libro)

    def devolver_libro(self, isbn):
        """
        Elimina un libro de la lista de préstamos basándose en su ISBN.

        Returns:
            bool: True si se encontró y eliminó, False en caso contrario.
        """
        for i, libro in enumerate(self.libros_prestados):
            if libro.isbn == isbn:
                del self.libros_prestados[i]
                return True
        return False

    def listar_prestamos(self):
        """Devuelve una copia de la lista de libros prestados."""
        return self.libros_prestados.copy()

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


class Biblioteca:
    """
    Clase principal que gestiona todo el sistema: catálogo, usuarios y préstamos.
    """

    def __init__(self):
        """Inicializa la biblioteca con colecciones vacías."""
        # REQUISITO: Diccionario para almacenar libros con ISBN como clave.
        # Permite búsqueda O(1) por ISBN.
        self.catalogo_libros = {}

        # REQUISITO: Conjunto para manejar los IDs de usuarios únicos.
        # Los sets no permiten duplicados, asegurando integridad de IDs.
        self.ids_registrados = set()

        # Diccionario auxiliar para acceder al objeto Usuario por su ID rápidamente
        self.usuarios_registrados = {}

    # --- Gestión de Libros ---

    def añadir_libro(self, libro):
        """
        Añade un libro al catálogo.

        Args:
            libro (Libro): Objeto Libro a añadir.

        Returns:
            bool: True si se añadió, False si el ISBN ya existe.
        """
        if libro.isbn in self.catalogo_libros:
            print(f"Error: El libro con ISBN {libro.isbn} ya existe en la biblioteca.")
            return False
        self.catalogo_libros[libro.isbn] = libro
        print(f"Libro añadido: {libro.titulo}")
        return True

    def quitar_libro(self, isbn):
        """
        Elimina un libro del catálogo.

        Args:
            isbn (str): ISBN del libro a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        if isbn in self.catalogo_libros:
            del self.catalogo_libros[isbn]
            print(f"Libro con ISBN {isbn} eliminado del catálogo.")
            return True
        print(f"Error: No se encontró el libro con ISBN {isbn}.")
        return False

    # --- Gestión de Usuarios ---

    def registrar_usuario(self, nombre, id_usuario):
        """
        Registra un nuevo usuario en el sistema.

        Args:
            nombre (str): Nombre del usuario.
            id_usuario (str/int): ID único.

        Returns:
            bool: True si se registró, False si el ID ya existe.
        """
        # Usamos el set para verificar unicidad rápidamente
        if id_usuario in self.ids_registrados:
            print(f"Error: El ID de usuario {id_usuario} ya está registrado.")
            return False

        nuevo_usuario = Usuario(nombre, id_usuario)
        self.usuarios_registrados[id_usuario] = nuevo_usuario
        self.ids_registrados.add(id_usuario)  # Añadimos al conjunto de control
        print(f"Usuario registrado: {nombre}")
        return True

    def dar_baja_usuario(self, id_usuario):
        """
        Da de baja a un usuario.

        Args:
            id_usuario: ID del usuario a eliminar.

        Returns:
            bool: True si se eliminó, False si no existía.
        """
        if id_usuario in self.ids_registrados:
            # Verificar si tiene libros prestados antes de borrar (opcional pero recomendado)
            usuario = self.usuarios_registrados[id_usuario]
            if usuario.libros_prestados:
                print(f"Advertencia: El usuario {usuario.nombre} tiene libros pendientes. Se dará de baja igualmente.")

            del self.usuarios_registrados[id_usuario]
            self.ids_registrados.remove(id_usuario)  # Eliminamos del conjunto
            print(f"Usuario {id_usuario} dado de baja.")
            return True
        print(f"Error: Usuario {id_usuario} no encontrado.")
        return False

    # --- Gestión de Préstamos ---

    def prestar_libro(self, isbn, id_usuario):
        """
        Gestiona el préstamo de un libro a un usuario.

        Args:
            isbn (str): ISBN del libro.
            id_usuario: ID del usuario.
        """
        # 1. Validar existencia del libro
        if isbn not in self.catalogo_libros:
            print("Error: Libro no encontrado en el catálogo.")
            return

        # 2. Validar existencia del usuario
        if id_usuario not in self.ids_registrados:
            print("Error: Usuario no registrado.")
            return

        libro = self.catalogo_libros[isbn]
        usuario = self.usuarios_registrados[id_usuario]

        # 3. Verificar disponibilidad (si el libro está ya en la lista de algún usuario)
        # En un sistema real, esto podría requerir buscar en todos los usuarios,
        # pero aquí asumimos que si está en la lista del usuario actual o no está 'disponible'.
        # Para simplificar y cumplir el requisito, verificaremos si el libro está prestado a CUALQUIER usuario.
        esta_prestado = False
        for user in self.usuarios_registrados.values():
            for l_prestado in user.libros_prestados:
                if l_prestado.isbn == isbn:
                    esta_prestado = True
                    break

        if esta_prestado:
            print(f"Error: El libro '{libro.titulo}' no está disponible (ya prestado).")
            return

        # 4. Realizar el préstamo
        usuario.prestar_libro(libro)
        print(f"Préstamo exitoso: {libro.titulo} -> {usuario.nombre}")

    def devolver_libro(self, isbn, id_usuario):
        """
        Gestiona la devolución de un libro.

        Args:
            isbn (str): ISBN del libro.
            id_usuario: ID del usuario.
        """
        if id_usuario not in self.ids_registrados:
            print("Error: Usuario no registrado.")
            return

        usuario = self.usuarios_registrados[id_usuario]

        if usuario.devolver_libro(isbn):
            print(f"Devolución exitosa: ISBN {isbn} por {usuario.nombre}")
        else:
            print(f"Error: El usuario {usuario.nombre} no tiene el libro con ISBN {isbn}.")

    # --- Búsquedas ---

    def buscar_libros(self, criterio, tipo="titulo"):
        """
        Busca libros en el catálogo.

        Args:
            criterio (str): Texto a buscar.
            tipo (str): 'titulo', 'autor' o 'categoria'.

        Returns:
            list: Lista de libros encontrados.
        """
        resultados = []
        criterio = criterio.lower()

        for libro in self.catalogo_libros.values():
            coincide = False
            if tipo == "titulo" and criterio in libro.titulo.lower():
                coincide = True
            elif tipo == "autor" and criterio in libro.autor.lower():
                coincide = True
            elif tipo == "categoria" and criterio in libro.categoria.lower():
                coincide = True

            if coincide:
                resultados.append(libro)

        return resultados

    def listar_prestamos_usuario(self, id_usuario):
        """
        Muestra los libros actualmente prestados a un usuario.

        Args:
            id_usuario: ID del usuario.
        """
        if id_usuario not in self.ids_registrados:
            print("Usuario no encontrado.")
            return

        usuario = self.usuarios_registrados[id_usuario]
        print(f"\n--- Libros prestados a {usuario.nombre} ---")
        if not usuario.libros_prestados:
            print("No tiene libros prestados.")
        else:
            for libro in usuario.libros_prestados:
                print(f"- {libro}")
        print("-----------------------------------------\n")


# ==========================================
# BLOQUE DE PRUEBAS (MAIN)
# ==========================================
if __name__ == "__main__":
    # 1. Inicializar el sistema
    mi_biblioteca = Biblioteca()

    print("=== 1. Añadiendo Libros ===")
    # Creación de objetos Libro (usando tupla internamente)
    l1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "978-0001")
    l2 = Libro("El Principito", "Antoine de Saint-Exupéry", "Infantil", "978-0002")
    l3 = Libro("1984", "George Orwell", "Distopía", "978-0003")

    mi_biblioteca.añadir_libro(l1)
    mi_biblioteca.añadir_libro(l2)
    mi_biblioteca.añadir_libro(l3)
    # Intento añadir duplicado
    mi_biblioteca.añadir_libro(Libro("Libro Duplicado", "Autor", "Cat", "978-0001"))

    print("\n=== 2. Registrando Usuarios ===")
    mi_biblioteca.registrar_usuario("Ana Pérez", 101)
    mi_biblioteca.registrar_usuario("Carlos Ruiz", 102)
    # Intento registrar ID duplicado
    mi_biblioteca.registrar_usuario("Usuario Duplicado", 101)

    print("\n=== 3. Buscando Libros ===")
    encontrados = mi_biblioteca.buscar_libros("orwell", tipo="autor")
    print(f"Búsqueda por autor 'orwell': {encontrados}")

    encontrados = mi_biblioteca.buscar_libros("novela", tipo="categoria")
    print(f"Búsqueda por categoría 'novela': {encontrados}")

    print("\n=== 4. Realizando Préstamos ===")
    mi_biblioteca.prestar_libro("978-0001", 101)  # Ana presta Cien Años
    mi_biblioteca.prestar_libro("978-0002", 101)  # Ana presta Principito
    mi_biblioteca.prestar_libro("978-0001", 102)  # Carlos intenta prestar el mismo libro (debe fallar)

    print("\n=== 5. Listando Préstamos ===")
    mi_biblioteca.listar_prestamos_usuario(101)
    mi_biblioteca.listar_prestamos_usuario(102)

    print("\n=== 6. Devolviendo Libros ===")
    mi_biblioteca.devolver_libro("978-0001", 101)  # Ana devuelve Cien Años
    mi_biblioteca.prestar_libro("978-0001", 102)  # Ahora Carlos sí puede prestarlo

    print("\n=== 7. Estado Final ===")
    mi_biblioteca.listar_prestamos_usuario(101)
    mi_biblioteca.listar_prestamos_usuario(102)

    print("\n=== 8. Dando de Baja ===")
    mi_biblioteca.dar_baja_usuario(102)