import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
#ejemplo
# ---------------------------
# CONEXIÓN A BASE DE DATOS,
# ---------------------------

conexion = sqlite3.connect("cajero.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha TEXT NOT NULL
)
""")

conexion.commit()
# ejemplo
# ---------------------------
# FUNCIONES
# ---------------------------

def obtener_saldo():
    cursor.execute("SELECT tipo, monto FROM movimientos")
    registros = cursor.fetchall()
    saldo = 0

    for tipo, monto in registros:
        if tipo == "Deposito":
            saldo += monto
        else:
            saldo -= monto

    return saldo


def actualizar_saldo_label():
    saldo = obtener_saldo()
    label_saldo.config(text=f"Saldo actual: ${saldo:.2f}")


def depositar():
    try:
        monto = float(entry_monto.get())
        if monto <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero")
            return

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute(
            "INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)",
            ("Deposito", monto, fecha)
        )
        conexion.commit()

        messagebox.showinfo("Éxito", "Depósito realizado correctamente")
        entry_monto.delete(0, tk.END)
        actualizar_saldo_label()
        cargar_historial()

    except:
        messagebox.showerror("Error", "Ingrese un número válido")


def retirar():
    try:
        monto = float(entry_monto.get())
        saldo = obtener_saldo()

        if monto <= 0:
            messagebox.showerror("Error", "El monto debe ser mayor a cero")
        elif monto > saldo:
            messagebox.showerror("Error", "Fondos insuficientes")
        else:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            cursor.execute(
                "INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)",
                ("Retiro", monto, fecha)
            )
            conexion.commit()

            messagebox.showinfo("Éxito", "Retiro realizado correctamente")
            entry_monto.delete(0, tk.END)
            actualizar_saldo_label()
            cargar_historial()

    except:
        messagebox.showerror("Error", "Ingrese un número válido")


def cargar_historial():
    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("SELECT * FROM movimientos")
    registros = cursor.fetchall()

    for fila in registros:
        tabla.insert("", tk.END, values=fila)

# 
# ---------------------------
# INTERFAZ GRÁFICA
# ---------------------------

ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.geometry("600x500")
ventana.resizable(False, False)

titulo = tk.Label(ventana, text="CAJERO AUTOMÁTICO", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

label_saldo = tk.Label(ventana, text="", font=("Arial", 12))
label_saldo.pack()

frame_operaciones = tk.Frame(ventana)
frame_operaciones.pack(pady=10)

tk.Label(frame_operaciones, text="Monto:").grid(row=0, column=0, padx=5)

entry_monto = tk.Entry(frame_operaciones)
entry_monto.grid(row=0, column=1, padx=5)

tk.Button(frame_operaciones, text="Depositar", bg="green", fg="white", command=depositar).grid(row=1, column=0, pady=10)
tk.Button(frame_operaciones, text="Retirar", bg="red", fg="white", command=retirar).grid(row=1, column=1, pady=10)

# TABLA HISTORIAL
columnas = ("ID", "Tipo", "Monto", "Fecha")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=130)

tabla.pack(pady=20)

# Inicializar datos
actualizar_saldo_label()
cargar_historial()

ventana.mainloop()

conexion.close()
