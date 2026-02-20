import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import tkinter.simpledialog as sd
# ---------------------------
# INICIO DE SESIÓN
# ---------------------------

USUARIO = "alejo"
CONTRASEÑA = "1234"

def iniciar_sesion():
    usuario = sd.askstring("Inicio de sesión", "Ingrese su usuario:")
    if usuario != USUARIO:
        messagebox.showerror("Error", "Usuario incorrecto")
        return False

    contrasena = sd.askstring("Inicio de sesión", "Ingrese su contraseña:", show="*")
    if contrasena != CONTRASEÑA:
        messagebox.showerror("Error", "Contraseña incorrecta")
        return False

    messagebox.showinfo("Bienvenido", f"Bienvenido {usuario}")
    return True
# Intentar iniciar sesión antes de abrir la GUI
if not iniciar_sesion():
    exit()  # Cierra el programa si falla el inicio de sesión

# ---------------------------
# CONEXIÓN A BASE DE DATOS
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

# ---------------------------
# FUNCIONES
# ---------------------------
def obtener_saldo():
    cursor.execute("SELECT tipo, monto FROM movimientos")
    registros = cursor.fetchall()
    saldo = 0
    for tipo, monto in registros:
        saldo += monto if tipo == "Deposito" else -monto
    return saldo

def actualizar_saldo_label():
    saldo = obtener_saldo()
    label_saldo.config(text=f"Saldo actual: ${saldo:.2f}")

def cargar_historial():
    for fila in tabla.get_children():
        tabla.delete(fila)
    cursor.execute("SELECT * FROM movimientos")
    registros = cursor.fetchall()
    for i, fila in enumerate(registros):
        if i % 2 == 0:
            tabla.insert("", tk.END, values=fila, tags=('par',))
        else:
            tabla.insert("", tk.END, values=fila, tags=('impar',))

def depositar_validado():
    try:
        monto = float(entry_monto.get())
        if monto <= 0:
            messagebox.showerror("Error", "Monto inválido")
            return
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)", ("Deposito", monto, fecha))
        conexion.commit()
        messagebox.showinfo("Éxito", "Depósito realizado correctamente")
        entry_monto.delete(0, tk.END)
        actualizar_saldo_label()
        cargar_historial()
    except:
        messagebox.showerror("Error", "Ingrese un número válido")

def retirar_validado():
    try:
        monto = float(entry_monto.get())
        saldo = obtener_saldo()
        if monto <= 0:
            messagebox.showerror("Error", "Monto inválido")
            return
        if monto > saldo:
            messagebox.showerror("Error", "Fondos insuficientes")
            return
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)", ("Retiro", monto, fecha))
        conexion.commit()
        messagebox.showinfo("Éxito", "Retiro realizado correctamente")
        entry_monto.delete(0, tk.END)
        actualizar_saldo_label()
        cargar_historial()
    except:
        messagebox.showerror("Error", "Ingrese un número válido")

# ---------------------------
# INTERFAZ GRÁFICA NEGRA
# ---------------------------
ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.geometry("750x550")
ventana.resizable(False, False)
ventana.config(bg="#1c1c1c")  # fondo negro

# Título
titulo = tk.Label(ventana, text="CAJERO AUTOMÁTICO", font=("Arial", 22, "bold"),
                  bg="#1c1c1c", fg="#ffffff")  # letras blancas
titulo.pack(pady=15)

# Saldo
label_saldo = tk.Label(ventana, text="", font=("Arial", 16, "bold"),
                       bg="#1c1c1c", fg="#00ff00")  # saldo verde neón
label_saldo.pack(pady=5)

# Frame operaciones
frame_operaciones = tk.LabelFrame(ventana, text="Operaciones", font=("Arial", 12, "bold"),
                                  bg="#2b2b2b", fg="#ffffff", padx=10, pady=10)
frame_operaciones.pack(pady=10, padx=20, fill="x")

tk.Label(frame_operaciones, text="Monto:", font=("Arial", 12),
         bg="#2b2b2b", fg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
entry_monto = tk.Entry(frame_operaciones, font=("Arial", 12), bg="#333333", fg="#ffffff")
entry_monto.grid(row=0, column=1, padx=5, pady=5)

# Función hover
def on_enter(e, color):
    e.widget['background'] = color

def on_leave(e, color):
    e.widget['background'] = color

# Botones con hover
btn_depositar = tk.Button(frame_operaciones, text="Depositar", bg="#4CAF50", fg="white",
          font=("Arial", 12, "bold"), width=12, command=depositar_validado)
btn_depositar.grid(row=1, column=0, pady=10, padx=5)
btn_depositar.bind("<Enter>", lambda e: on_enter(e, "#45a049"))
btn_depositar.bind("<Leave>", lambda e: on_leave(e, "#4CAF50"))

btn_retirar = tk.Button(frame_operaciones, text="Retirar", bg="#F44336", fg="white",
          font=("Arial", 12, "bold"), width=12, command=retirar_validado)
btn_retirar.grid(row=1, column=1, pady=10, padx=5)
btn_retirar.bind("<Enter>", lambda e: on_enter(e, "#da190b"))
btn_retirar.bind("<Leave>", lambda e: on_leave(e, "#F44336"))

# Frame historial
frame_historial = tk.LabelFrame(ventana, text="Historial de Movimientos", font=("Arial", 12, "bold"),
                                bg="#2b2b2b", fg="#ffffff", padx=10, pady=10)
frame_historial.pack(pady=15, padx=20, fill="both", expand=True)

columnas = ("ID", "Tipo", "Monto", "Fecha")
tabla = ttk.Treeview(frame_historial, columns=columnas, show="headings")
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=150, anchor="center")

# Colores filas alternadas para fondo oscuro
tabla.tag_configure('par', background='#333333', foreground="#ffffff")
tabla.tag_configure('impar', background='#444444', foreground="#ffffff")

tabla.pack(side=tk.LEFT, fill="both", expand=True)

scroll = ttk.Scrollbar(frame_historial, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill="y")

# Inicializar datos
actualizar_saldo_label()
cargar_historial()

ventana.mainloop()
conexion.close()