import tkinter as tk
from tkinter import messagebox

class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
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
        return f"Titulo: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Estado: {estado}"

class Miembro:
    def __init__(self, nombre, id_miembro):
        self.nombre = nombre
        self.id_miembro = id_miembro

    def __str__(self):
        return f"Miembro: {self.nombre}, ID: {self.id_miembro}"

class Biblioteca:
    def __init__(self):
        self.catalogo = []
        self.miembros = []

    def anadir_libro(self, libro):
        self.catalogo.append(libro)
        return f"Libro '{libro.titulo}' agregado al catálogo."

    def prestar_libro(self, isbn, id_miembro):
        miembro = next((m for m in self.miembros if m.id_miembro == id_miembro), None)
        if miembro is None:
            return "Miembro no encontrado."
        for libro in self.catalogo:
            if libro.isbn == isbn:
                return libro.prestar(miembro)
        return "Libro no encontrado."

    def devolver_libro(self, isbn):
        for libro in self.catalogo:
            if libro.isbn == isbn:
                return libro.devolver()
        return "Libro no encontrado."

    def actualizar_libro(self, isbn):
        for libro in self.catalogo:
            if libro.isbn == isbn:
                libro.prestado_a = None
                return f"Estado del libro '{libro.titulo}' actualizado."
        return "Libro no encontrado."
    
    def mostrar_catalogo(self):
        return "\n".join(str(libro) for libro in self.catalogo) if self.catalogo else "No hay libros en el catálogo."
    
    def agregar_miembro(self, miembro):
        self.miembros.append(miembro)
        return f"Miembro '{miembro.nombre}' agregado a la biblioteca."

    def mostrar_miembros(self):
        return "\n".join(str(miembro) for miembro in self.miembros) if self.miembros else "No hay miembros registrados."
    
    

def prestar_libro():
    entry_isbn=input("Ingrese el ISBN del libro a prestar: ")
    isbn = entry_isbn.get()
    id_miembro = entry_id_prestamo.get()
    biblioteca = Biblioteca()
    messagebox.showinfo("Resultado", biblioteca.prestar_libro(isbn, id_miembro))
    tk.Label(frame, text="ID Miembro para Préstamo:").grid(row=11, column=0)
    entry_id_prestamo = tk.Entry(frame)
    entry_id_prestamo.grid(row=11, column=1)

    
    btn_prestar = tk.Button(frame, text="Prestar Libro")
    btn_prestar.configure(command=prestar_libro)
    
def agregar_libro():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Libro")

    tk.Label(ventana_agregar, text="Título:").grid(row=0, column=0)
    entry_titulo = tk.Entry(ventana_agregar)
    entry_titulo.grid(row=0, column=1)

    tk.Label(ventana_agregar, text="Autor:").grid(row=1, column=0)
    entry_autor = tk.Entry(ventana_agregar)
    entry_autor.grid(row=1, column=1)

    tk.Label(ventana_agregar, text="ISBN:").grid(row=2, column=0)
    entry_isbn = tk.Entry(ventana_agregar)
    entry_isbn.grid(row=2, column=1)

    def anadir_libro():
        titulo = entry_titulo.get()
        autor = entry_autor.get()
        isbn = entry_isbn.get()
        if titulo and autor and isbn:
            libro = Libro(titulo, autor, isbn)
            biblioteca.anadir_libro(libro)
            messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.")
            ventana_agregar.destroy()  # Cierra la ventana después de agregar
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

    tk.Button(ventana_agregar, text="Agregar", command=anadir_libro).grid(row=3, column=0, columnspan=2, pady=10)
    


def devolver_libro():
    isbn = entry_isbn.get()
    messagebox.showinfo("Resultado", biblioteca.devolver_libro(isbn))

def mostrar_catalogo():
    messagebox.showinfo("Catálogo", biblioteca.mostrar_catalogo())
    
def abrir_actualizar_libro():
    ventana_actualizar = tk.Toplevel(root)
    ventana_actualizar.title("Actualizar Libro")

    tk.Label(ventana_actualizar, text="ISBN del Libro:").grid(row=0, column=0)
    entry_isbn_buscar = tk.Entry(ventana_actualizar)
    entry_isbn_buscar.grid(row=0, column=1)

    tk.Label(ventana_actualizar, text="Nuevo Título:").grid(row=1, column=0)
    entry_nuevo_titulo = tk.Entry(ventana_actualizar)
    entry_nuevo_titulo.grid(row=1, column=1)

    tk.Label(ventana_actualizar, text="Nuevo Autor:").grid(row=2, column=0)
    entry_nuevo_autor = tk.Entry(ventana_actualizar)
    entry_nuevo_autor.grid(row=2, column=1)

    def actualizar_libro():
        isbn = entry_isbn_buscar.get()
        nuevo_titulo = entry_nuevo_titulo.get()
        nuevo_autor = entry_nuevo_autor.get()

        for libro in biblioteca.catalogo:
            if libro.isbn == isbn:
                if nuevo_titulo:
                    libro.titulo = nuevo_titulo
                if nuevo_autor:
                    libro.autor = nuevo_autor
                messagebox.showinfo("Éxito", f"Libro con ISBN {isbn} actualizado correctamente.")
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

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

btn_agregar = tk.Button(frame, text="Agregar Libro", command=agregar_libro)
btn_agregar.grid(row=0, column=0, columnspan=1)

btn_agregar = tk.Button(frame, text="Actualizar Libro", command=abrir_actualizar_libro)
btn_agregar.grid(row=0, column=1, columnspan=1)

btn_agregar = tk.Button(frame, text="Agregar Miembro ", command=abrir_agregar_miembro)
btn_agregar.grid(row=0, column=2, columnspan=1)

btn_prestar = tk.Button(frame, text="Prestar Libro", command=prestar_libro)
btn_prestar.grid(row=1, column=0, columnspan=1)

btn_devolver = tk.Button(frame, text="Devolver Libro", command=devolver_libro)
btn_devolver.grid(row=1, column=1, columnspan=1)

btn_mostrar = tk.Button(frame, text="Mostrar Catálogo", command=mostrar_catalogo)
btn_mostrar.grid(row=1, column=2, columnspan=1)

root.mainloop()



