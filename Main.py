import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk


class Libro:
    def __init__(self, titulo, autor, BookID):
        self.titulo = titulo
        self.autor = autor
        self.BookID = BookID
        self.prestado_a = None

    def prestar(self, miembro):
        if self.prestado_a is None:
            self.prestado_a = miembro
            return f"El libro '{self.titulo}' ha sido prestado a {miembro.nombre}."
        return f"El libro '{self.titulo}' ya está prestado a {self.prestado_a.nombre}."

    def devolver(self):
        if self.prestado_a is not None:
            nombre_miembro = self.prestado_a.nombre
            self.prestado_a = None
            return f"El libro '{self.titulo}' ha sido devuelto por {nombre_miembro}."
        return f"El libro '{self.titulo}' no estaba prestado."

    def __str__(self):
        estado = f"Prestado a {self.prestado_a.nombre}" if self.prestado_a else "Disponible"
        return f"Titulo: {self.titulo}, Autor: {self.autor}, BookID: {self.BookID}, Estado: {estado}"

class Miembro:
    def __init__(self, nombre, id_miembro):
        self.nombre = nombre
        self.id_miembro = id_miembro

    def __str__(self):
        return f"Miembro: {self.nombre}, ID: {self.id_miembro}"

class Biblioteca:
    db_name = 'database.db'
    def __init__(self):
        self.catalogo = []
        self.miembros = []

        self.create_table()
        
    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado

    
    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    libro TEXT NOT NULL,
                    bookID TEXT UNIQUE NOT NULL,
                    estado TEXT NOT NULL
                )'''
        self.run_query(query)
        
    def anadir_libro(self, libro):
        self.catalogo.append(libro)
        query = 'INSERT INTO libros VALUES (NULL, ?, ?, ?, "Disponible")'
        parametros = (libro.titulo, libro.autor, libro.BookID)
        self.run_query(query, parametros)
        
    def get_libros(self):
        
        ventana = tk.Toplevel()
        ventana.title("Lista de Libros")
        ventana.geometry("700x500")  # Ajustar tamaño

        # Crear Treeview (tabla)
        tree = ttk.Treeview(ventana, columns=("Nombre", "Autor", "BookID", "Estado"), show="headings")
        
        # Definir encabezados
        tree.heading("Nombre", text="Nombre")
        tree.heading("Autor", text="Autor")
        tree.heading("BookID", text="BookID")
        tree.heading("Estado", text="Estado")
        
        # Ajustar ancho de columnas
        tree.column("Nombre", width=200)
        tree.column("Autor", width=150)
        tree.column("BookID", width=100)
        tree.column("Estado", width=100)

        # Obtener datos de la base de datos
        query = 'SELECT nombre, libro, bookID, estado FROM libros ORDER BY nombre DESC'
        db_rows = self.run_query(query)

        # Insertar datos en la tabla
        for row in db_rows:
            tree.insert("", tk.END, values=row)

        # Ubicar tabla en ventana
        tree.pack(expand=True, fill="both")
        ventana.grab_set()
        
    def prestar_libro(self, BookID, id_miembro):
        miembro = next((m for m in self.miembros if m.id_miembro == id_miembro), None)
        if miembro is None:
            return "Miembro no encontrado."
        for libro in self.catalogo:
            if libro.BookID == BookID:
                return libro.prestar(miembro)
        return "Libro no encontrado."

    def devolver_libro(self, BookID):
        for libro in self.catalogo:
            if libro.BookID == BookID:
                return libro.devolver()
        return "Libro no encontrado."

    def actualizar_libro(self, BookID):
        for libro in self.catalogo:
            if libro.BookID == BookID:
                libro.prestado_a = None
                return f"Estado del libro '{libro.titulo}' actualizado."
        return "Libro no encontrado."
    
    
    def agregar_miembro(self, miembro):
        self.miembros.append(miembro)
        return f"Miembro '{miembro.nombre}' agregado a la biblioteca."

    def mostrar_miembros(self):
        return "\n".join(str(miembro) for miembro in self.miembros) if self.miembros else "No hay miembros registrados."
    
    


def agregar_libro():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Libro")

    tk.Label(ventana_agregar, text="Título:").grid(row=0, column=0)
    entry_titulo = tk.Entry(ventana_agregar)
    entry_titulo.grid(row=0, column=1)

    tk.Label(ventana_agregar, text="Autor:").grid(row=1, column=0)
    entry_autor = tk.Entry(ventana_agregar)
    entry_autor.grid(row=1, column=1)

    tk.Label(ventana_agregar, text="BookID:").grid(row=2, column=0)
    entry_BookID = tk.Entry(ventana_agregar)
    entry_BookID.grid(row=2, column=1)

    def anadir_libro():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        BookID = entry_BookID.get()
        if titulo and autor and BookID:
            libro = Libro(titulo, autor, BookID)
            biblioteca.anadir_libro(libro)
            messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.")
            ventana_agregar.destroy()  # Cierra la ventana después de agregar
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            
        

    tk.Button(ventana_agregar, text="Agregar", command=anadir_libro).grid(row=3, column=0, columnspan=2, pady=10)
    
def abrir_prestamo():
    ventana_prestamo = tk.Toplevel(root)
    ventana_prestamo.title("Prestar Libro")

    tk.Label(ventana_prestamo, text="BookID del Libro:").grid(row=0, column=0)
    entry_BookID = tk.Entry(ventana_prestamo)
    entry_BookID.grid(row=0, column=1)

    tk.Label(ventana_prestamo, text="ID del Miembro:").grid(row=1, column=0)
    entry_id_miembro = tk.Entry(ventana_prestamo)
    entry_id_miembro.grid(row=1, column=1)

    def prestar_libro():
        BookID = entry_BookID.get()
        id_miembro = entry_id_miembro.get()

        if not BookID or not id_miembro:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        resultado = biblioteca.prestar_libro(BookID, id_miembro)
        messagebox.showinfo("Resultado", resultado)
        ventana_prestamo.destroy()  # Cierra la ventana después de prestar el libro

    tk.Button(ventana_prestamo, text="Prestar", command=prestar_libro).grid(row=2, column=0, columnspan=2, pady=10)

def abrir_devolucion():
    ventana_devolucion = tk.Toplevel(root)
    ventana_devolucion.title("Devolver Libro")

    tk.Label(ventana_devolucion, text="BookID del Libro:").grid(row=0, column=0)
    entry_BookID_devolucion = tk.Entry(ventana_devolucion)
    entry_BookID_devolucion.grid(row=0, column=1)

    def devolver_libro():
        BookID = entry_BookID_devolucion.get()

        if not BookID:
            messagebox.showwarning("Error", "Debe ingresar el BookID del libro.")
            return

        resultado = biblioteca.devolver_libro(BookID)
        messagebox.showinfo("Resultado", resultado)
        ventana_devolucion.destroy() 

    tk.Button(ventana_devolucion, text="Devolver", command=devolver_libro).grid(row=1, column=0, columnspan=2, pady=10)


def mostrar_catalogo():

    biblioteca.get_libros()
    
def abrir_actualizar_libro():
    ventana_actualizar = tk.Toplevel(root)
    ventana_actualizar.title("Actualizar Libro")

    tk.Label(ventana_actualizar, text="BookID del Libro:").grid(row=0, column=0)
    entry_BookID_buscar = tk.Entry(ventana_actualizar)
    entry_BookID_buscar.grid(row=0, column=1)

    tk.Label(ventana_actualizar, text="Nuevo Título:").grid(row=1, column=0)
    entry_nuevo_titulo = tk.Entry(ventana_actualizar)
    entry_nuevo_titulo.grid(row=1, column=1)

    tk.Label(ventana_actualizar, text="Nuevo Autor:").grid(row=2, column=0)
    entry_nuevo_autor = tk.Entry(ventana_actualizar)
    entry_nuevo_autor.grid(row=2, column=1)

    def actualizar_libro():
        BookID = entry_BookID_buscar.get()
        nuevo_titulo = entry_nuevo_titulo.get()
        nuevo_autor = entry_nuevo_autor.get()

        for libro in biblioteca.catalogo:
            if libro.BookID == BookID:
                if nuevo_titulo:
                    libro.titulo = nuevo_titulo
                if nuevo_autor:
                    libro.autor = nuevo_autor
                messagebox.showinfo("Éxito", f"Libro con BookID {BookID} actualizado correctamente.")
                ventana_actualizar.destroy()
                return
        
        messagebox.showwarning("Error", "Libro no encontrado.")

    tk.Button(ventana_actualizar, text="Actualizar", command=actualizar_libro).grid(row=3, column=0, columnspan=2, pady=10)
    
def abrir_agregar_miembro():
    ventana_miembro = tk.Toplevel(root)
    ventana_miembro.title("Agregar Miembro")

    tk.Label(ventana_miembro, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(ventana_miembro)
    entry_nombre.grid(row=0, column=1)

    tk.Label(ventana_miembro, text="ID del Miembro:").grid(row=1, column=0)
    entry_id_miembro = tk.Entry(ventana_miembro)
    entry_id_miembro.grid(row=1, column=1)

    def agregar_miembro():
        nombre = entry_nombre.get()
        id_miembro = entry_id_miembro.get()

        if nombre and id_miembro:
            miembro = Miembro(nombre, id_miembro)
            biblioteca.agregar_miembro(miembro)
            messagebox.showinfo("Éxito", f"Miembro '{nombre}' agregado correctamente.")
            ventana_miembro.destroy()  
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    tk.Button(ventana_miembro, text="Agregar", command=agregar_miembro).grid(row=2, column=0, columnspan=2, pady=10)
    
# Configuración de la interfaz gráfica
biblioteca = Biblioteca()
root = tk.Tk()
root.title("Gestión de Biblioteca")
root.configure(bg="orange")  # Fondo negro para la ventana principal

# Crear frame dentro de la ventana principal
frame = tk.Frame(root, bg="black")  
frame = tk.Frame(root)
frame.pack(padx=100, pady=100)


btn_agregar = tk.Button(frame, text="Agregar Libro", command=agregar_libro)
btn_agregar.grid(row=0, column=0, columnspan=1)

btn_agregar = tk.Button(frame, text="Actualizar Libro", command=abrir_actualizar_libro)
btn_agregar.grid(row=0, column=1, columnspan=1)

btn_agregar = tk.Button(frame, text="Agregar Miembro ", command=abrir_agregar_miembro)
btn_agregar.grid(row=0, column=2, columnspan=1)

btn_prestar = tk.Button(frame, text="Prestar Libro", command=abrir_prestamo)
btn_prestar.grid(row=1, column=0, columnspan=1)

btn_devolver = tk.Button(frame, text="Devolver Libro", command=abrir_devolucion)
btn_devolver.grid(row=1, column=1, columnspan=1)

btn_mostrar = tk.Button(frame, text="Mostrar Catálogo", command=mostrar_catalogo)
btn_mostrar.grid(row=1, column=2, columnspan=1)

root.mainloop()



