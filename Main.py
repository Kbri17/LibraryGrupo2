import tkinter as tk
from tkinter import Image, messagebox
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime


class Libro:
    db_name = 'database.db'

    def __init__(self, titulo, autor, bookID):
        self.titulo = titulo
        self.autor = autor
        self.bookID = bookID
        self.disponible = True

    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resultado = cursor.execute(query, parametros)
            conn.commit()
        return resultado

    def prestar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def devolver(self, fecha_devolucion, fecha_limite):
        self.disponible = True
        if fecha_devolucion <= fecha_limite:
            return "Libro devuelto a tiempo. Se aplica un descuento del 15%."
        return "Libro devuelto fuera de tiempo."

    def prestarse(self, bookID, miembro_id):
        query0 = "SELECT estado FROM libros WHERE bookID = ?"
        parametros1 = (bookID,)
        estadoLibro = self.run_query(query0, parametros1).fetchone()

        if not estadoLibro:
            return f"Error: No se encontró un libro con el ID {bookID}."

        estado = estadoLibro[0]

        if estado == "Prestado":
            return f"El libro ya está prestado"

        query2 = "SELECT nombre FROM miembros WHERE id_miembro = ?"
        parametros2 = (miembro_id,)
        nombreMiembro = self.run_query(query2, parametros2).fetchone()

        if not nombreMiembro:
            return f"Error: No se encontró un miembro con el ID {miembro_id}."

        query3 = "UPDATE libros SET estado = ?, prestado_a = ? WHERE bookID = ?"
        parametros3 = ("Prestado", nombreMiembro[0], bookID,)
        self.run_query(query3, parametros3)

        return f"El libro ha sido prestado a {nombreMiembro[0]}."

    def devolverse(self, bookID, miembro_id, fecha_devolucion_str):
        queryS = "SELECT prestado_a FROM libros WHERE BookID = ?"
        parametrosS = (bookID,)
        estadoPrestado = self.run_query(queryS, parametrosS).fetchone()

        if not estadoPrestado or estadoPrestado[0] is None:
            return f"El libro no está prestado."

        queryN = "SELECT nombre FROM miembros WHERE id_miembro = ?"
        parametrosN = (miembro_id,)
        nombreN = self.run_query(queryN, parametrosN).fetchone()

        if not nombreN:
            return f"Error: No se encontró un miembro con el ID {miembro_id}."

        nombre_miembro = nombreN[0]

        fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%Y-%m-%d")
        fecha_limite = datetime.strptime(
            "2025-03-07", "%Y-%m-%d")  # Esta parte será la simulación de fecha límite

        resultado = self.devolver(fecha_devolucion, fecha_limite)

        if "a tiempo" in resultado:
            queryD = "UPDATE miembros SET descuento = 15 WHERE id_miembro = ?"
            parametrosD = (miembro_id,)
            self.run_query(queryD, parametrosD)
            resultado += " Se ha aplicado un descuento del 15% para la próxima vez."

        queryP = "UPDATE libros SET estado = ? WHERE BookID = ?"
        parametrosQ = ("Disponible", bookID,)
        self.run_query(queryP, parametrosQ)

        return f"{resultado} El libro con ID {bookID} ha sido devuelto por {nombre_miembro}."


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return f"Usuario: {self.nombre}"


class Miembro(Usuario):
    def __init__(self, nombre, id_miembro, tiempo_membresia):
        super().__init__(nombre)
        self.id_miembro = id_miembro
        self.tiempo_membresia = tiempo_membresia

    def pedir_membresia(self, meses):
        if self.tiempo_membresia > 0:
            return f'{self.nombre} ya tiene una membresía activa.'

        self.tiempo_membresia = meses

        query = "UPDATE miembros SET tiempo_membresia = ? WHERE id_miembro = ?"
        parametros = (self.tiempo_membresia, self.id_miembro)

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            conn.commit()

        return f'{self.nombre} ha obtenido una membresía por {meses} meses.'

    def renovar_membresia(self, meses):
        if meses <= 0:
            return 'La cantidad de meses debe ser mayor a 0'

        self.tiempo_membresia += meses

        query = "UPDATE miembros SET tiempo_membresia = ? WHERE id_miembro = ?"
        parametros = (self.tiempo_membresia, self.id_miembro)

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            conn.commit()

        return f'La membresía de {self.nombre} ha sido renovada por {meses} meses.'

    def eliminar_membresia(self):
        self.tiempo_membresia = 0

        query = "UPDATE miembros SET tiempo_membresia = 0 WHERE id_miembro = ?"
        parametros = (self.id_miembro,)

        with sqlite3.connect('database.db')as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            conn.commit()
        return f'La membresía de {self.nombre} ha sido eliminada.'


class Biblioteca:
    db_name = 'database.db'

    def __init__(self):
        self.catalogo = []
        self.miembros = []

        self.create_table()
        self.create_table2()

    def run_query(self, query, parametros=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                resultado = cursor.execute(query, parametros)
                conn.commit()
            return resultado
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            raise Exception(f"Error general en la base de datos: {e}")

    def create_table(self):
        query = '''CREATE TABLE IF NOT EXISTS libros (
                    nombre TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    bookID TEXT UNIQUE NOT NULL,
                    estado TEXT NOT NULL,
                    prestado_a TEXT 
                )'''
        self.run_query(query)

    def create_table2(self):
        query = '''CREATE TABLE IF NOT EXISTS miembros (
                    nombre TEXT NOT NULL,
                    id_miembro TEXT NOT NULL,
                    tiempo_membresia INTEGER NOT NULL
                )'''
        self.run_query(query)

    def anadir_libro(self, libro):
        self.catalogo.append(libro)
        query = 'INSERT INTO libros VALUES ( ?, ?, ?, "Disponible", "")'
        parametros = (libro.titulo, libro.autor, libro.bookID)
        self.run_query(query, parametros)

    def get_libros(self):

        ventana = tk.Toplevel()
        ventana.title("Lista de Libros")
        ventana.geometry("700x500")

        tree = ttk.Treeview(ventana, columns=(
            "Nombre", "Autor", "BookID", "Estado"), show="headings")

        tree.heading("Nombre", text="Nombre")
        tree.heading("Autor", text="Autor")
        tree.heading("BookID", text="BookID")
        tree.heading("Estado", text="Estado")

        tree.column("Nombre", width=200)
        tree.column("Autor", width=150)
        tree.column("BookID", width=100)
        tree.column("Estado", width=100)

        try:
            query = 'SELECT nombre, autor , bookID, estado FROM libros ORDER BY bookID DESC'
            db_rows = self.run_query(query)

            for row in db_rows:
                tree.insert("", tk.END, values=row)

            tree.pack(expand=True, fill="both")
            ventana.grab_set()

        except Exception as e:
            print(f"No hay libros disponibles")

    def actualizar_libro(self, libro):

        query = 'UPDATE libros SET nombre= ? , autor = ? WHERE bookID = ?'
        parametros = (libro.titulo, libro.autor, libro.bookID,)
        self.run_query(query, parametros)

        messagebox.showinfo(
            "Éxito", f"Libro con BookID {libro.bookID}  actualizado correctamente.")

    def agregar_miembro(self, nombre, id_miembro):
        query = 'INSERT INTO miembros VALUES ( ?, ?, 1 )'
        parametros = (nombre, id_miembro,)
        self.run_query(query, parametros)

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
        try:
            titulo = entry_titulo.get()
            autor = entry_autor.get()
            BookID = entry_BookID.get()
            if titulo and autor and BookID:
                libro = Libro(titulo, autor, BookID)
                biblioteca.anadir_libro(libro)
                messagebox.showinfo(
                    "Éxito", f"Libro '{titulo}' agregado correctamente.")
                ventana_agregar.destroy()
            else:
                messagebox.showwarning(
                    "Error", "Todos los campos son obligatorios.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al agregar el libro ,Intente nuevamente")

    tk.Button(ventana_agregar, text="Agregar", command=anadir_libro).grid(
        row=3, column=0, columnspan=2, pady=10)


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
            messagebox.showwarning(
                "Error", "Todos los campos son obligatorios.")
            return

        libro = Libro("", "", BookID)
        resultado = libro.prestarse(BookID, id_miembro)
        messagebox.showinfo("Resultado", resultado)
        ventana_prestamo.destroy()

    tk.Button(ventana_prestamo, text="Prestar", command=prestar_libro).grid(
        row=2, column=0, columnspan=2, pady=10)


def abrir_devolucion():
    ventana_devolucion = tk.Toplevel(root)
    ventana_devolucion.title("Devolver Libro")

    tk.Label(ventana_devolucion, text="BookID del Libro:").grid(row=0, column=0)
    entry_BookID_devolucion = tk.Entry(ventana_devolucion)
    entry_BookID_devolucion.grid(row=0, column=1)

    tk.Label(ventana_devolucion, text="Nombre del Miembro:").grid(
        row=1, column=0)
    entry_BookID_devolucion = tk.Entry(ventana_devolucion)
    entry_BookID_devolucion.grid(row=1, column=1)

    def devolver_libro():
        BookID = entry_BookID_devolucion.get()
        miembro_id = entry_BookID_devolucion.get()

        if not BookID or not miembro_id:
            messagebox.showwarning(
                "Error", "Todos los campos son obligatorios.")
            return

        libro = Libro("", "", BookID)
        resultado = libro.devolverse(BookID, miembro_id)
        messagebox.showinfo("Resultado", resultado)
        ventana_devolucion.destroy()

    tk.Button(ventana_devolucion, text="Devolver", command=devolver_libro).grid(
        row=2, column=0, columnspan=2, pady=10)


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

        if not BookID or not nuevo_titulo or not nuevo_autor:
            messagebox.showwarning(
                "Error", "Todos los campos son obligatorios.")
            return

        libro = Libro(nuevo_titulo, nuevo_autor, BookID)
        biblioteca.actualizar_libro(libro)
        ventana_actualizar.destroy()

    tk.Button(ventana_actualizar, text="Actualizar", command=actualizar_libro).grid(
        row=3, column=0, columnspan=2, pady=10)


def abrir_agregar_miembro():
    ventana_miembro = tk.Toplevel(root)
    ventana_miembro.title("Gestión de Miembros")

    tk.Label(ventana_miembro, text="Nombre:").grid(row=0, column=0)
    entry_nombre = tk.Entry(ventana_miembro)
    entry_nombre.grid(row=0, column=1)

    tk.Label(ventana_miembro, text="ID del Miembro:").grid(row=1, column=0)
    entry_id_miembro = tk.Entry(ventana_miembro)
    entry_id_miembro.grid(row=1, column=1)

    tk.Label(ventana_miembro,
             text="Fecha de Vencimiento (YYYY-MM-DD):").grid(row=2, column=0)
    entry_fecha = tk.Entry(ventana_miembro)
    entry_fecha.grid(row=2, column=1)

    def agregar_miembro():
        nombre = entry_nombre.get()
        id_miembro = entry_id_miembro.get()

        if nombre and id_miembro:
            if agregar_miembro(nombre, id_miembro):
                messagebox.showinfo(
                    "Éxito", f"Mientro '{nombre}' agregado correctamente.")
            else:
                messagebox.showerror(
                    "Error", "Todos los campos son obligatorios.")
            ventana_miembro.destroy()
        else:
            messagebox.showwarning(
                "Error", "Todos los campos son obligatorios.")

    def agregar_membresia():
        id_miembro = entry_id_miembro.get()
        fecha_vencimiento = entry_fecha_vencimiento.get()
        if not id_miembro or not fecha_vencimiento:
            messagebox.showwarning(
                "Error", "Todos los campos son obligatorios.")
            return
        query = "UPDATE miembros SET tiempo_membresia = ? WHERE id_miembro = ?"
        parametros = (fecha_vencimiento, id_miembro)
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            conn.commit()
        messagebox.showinfo(
            "Éxito", f"Membresía actualizada para el miembro {id_miembro} hasta {fecha_vencimiento}.")

    ventana = tk.Toplevel(root)
    ventana.title("Agregar Miembro")

    tk.Label(ventana, text="ID Miembro:").grid(row=0, column=0)
    entry_id_miembro = tk.Entry(ventana)
    entry_id_miembro.grid(row=0, column=1)

    tk.Label(ventana, text="Fecha de Vencimiento (YYYY-MM-DD):").grid(row=1, column=0)
    entry_fecha_vencimiento = tk.Entry(ventana)
    entry_fecha_vencimiento.grid(row=1, column=1)

    tk.Button(ventana, text="Agregar Membresía", command=agregar_membresia).grid(
        row=2, column=0, columnspan=2, pady=10)

    def renovar_membresia():
        id_miembro = entry_id_miembro.get()
        fecha_vencimiento = entry_fecha.get()

        if not id_miembro or not fecha_vencimiento:
            messagebox.showerror(
                "Error", "ID y Fecha de Vencimiento son obligatorios")
            return

        messagebox.showinfo("Éxito", "Membresía renovada correctamente.")

    def eliminar_membresia():
        id_miembro = entry_id_miembro.get()

        if not id_miembro:
            messagebox.showerror("Error", "ID del miembro es obligatorio")
            return

        messagebox.showinfo("Eliminado", "Membresía eliminada correctamente.")

    tk.Button(ventana_miembro, text="Agregar",
              command=agregar_membresia).grid(row=3, column=0, pady=10)
    tk.Button(ventana_miembro, text="Renovar",
              command=renovar_membresia).grid(row=3, column=1, pady=10)
    tk.Button(ventana_miembro, text="Eliminar",
              command=eliminar_membresia).grid(row=3, column=2, pady=10)


biblioteca = Biblioteca()
root = tk.Tk()
root.title("Gestión de Biblioteca")
root.geometry("626x351")


imagen_fondo = Image.open("biblio.png")
imagen_fondo = imagen_fondo.resize((626, 351))
root.imagen_tk = ImageTk.PhotoImage(imagen_fondo)

fondo_label = tk.Label(root, image=root.imagen_tk)
fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg="orange")
frame.place(relx=0.5, rely=0.5, anchor="center")

icon_agregar = Image.open("agregar_libro.png").resize((32, 32))
icon_actualizar = Image.open("actualizar.png").resize((32, 32))
icon_miembro = Image.open("agregar_miembro.png").resize((32, 32))
icon_prestar = Image.open("prestar_libro.png").resize((32, 32))
icon_devolver = Image.open("devolver_libro.png").resize((32, 32))
icon_mostrar = Image.open("catalogo.png").resize((32, 32))

root.icon_agregar_tk = ImageTk.PhotoImage(icon_agregar)
root.icon_actualizar_tk = ImageTk.PhotoImage(icon_actualizar)
root.icon_miembro_tk = ImageTk.PhotoImage(icon_miembro)
root.icon_prestar_tk = ImageTk.PhotoImage(icon_prestar)
root.icon_devolver_tk = ImageTk.PhotoImage(icon_devolver)
root.icon_mostrar_tk = ImageTk.PhotoImage(icon_mostrar)

btn_agregar = tk.Button(frame, text="Agregar Libro",
                        image=root.icon_agregar_tk, compound="left", command=agregar_libro)
btn_agregar.grid(row=0, column=0, padx=5, pady=5)

btn_actualizar = tk.Button(frame, text="Actualizar Libro",
                           image=root.icon_actualizar_tk, compound="left", command=abrir_actualizar_libro)
btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

btn_miembro = tk.Button(frame, text="Agregar Miembro", image=root.icon_miembro_tk,
                        compound="left", command=abrir_agregar_miembro)
btn_miembro.grid(row=0, column=2, padx=5, pady=5)

btn_prestar = tk.Button(frame, text="Prestar Libro",
                        image=root.icon_prestar_tk, compound="left", command=abrir_prestamo)
btn_prestar.grid(row=1, column=0, padx=5, pady=5)

btn_devolver = tk.Button(frame, text="Devolver Libro",
                         image=root.icon_devolver_tk, compound="left", command=abrir_devolucion)
btn_devolver.grid(row=1, column=1, padx=5, pady=5)

btn_mostrar = tk.Button(frame, text="Mostrar Catálogo",
                        image=root.icon_mostrar_tk, compound="left", command=mostrar_catalogo)
btn_mostrar.grid(row=1, column=2, padx=5, pady=5)

root.mainloop()
