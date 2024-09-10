import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Conexión a la base de datos
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="logistica"
    )

# Funciones para manejar los envíos
def agregar_envio():
    numero_seguimiento = entry_numero_seguimiento.get()
    origen = entry_origen.get()
    destino = entry_destino.get()
    fecha_entrega_prevista = entry_fecha_entrega_prevista.get()
    
    if not numero_seguimiento or not origen or not destino or not fecha_entrega_prevista:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Envios (NumeroSeguimiento, Origen, Destino, FechaEntregaPrevista) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (numero_seguimiento, origen, destino, fecha_entrega_prevista))
    conn.commit()
    conn.close()
    actualizar_lista_envios()
    messagebox.showinfo("Éxito", "Envío agregado correctamente")

def actualizar_lista_envios():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Envios")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def actualizar_envio():
    selected_item = tree.selection()[0]
    envio_id = tree.item(selected_item)["values"][0]
    nuevo_estado = combo_estado.get()
    
    if not nuevo_estado:
        messagebox.showerror("Error", "Debe seleccionar un estado")
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = "UPDATE Envios SET Estado = %s WHERE ID = %s"
    cursor.execute(sql, (nuevo_estado, envio_id))
    conn.commit()
    conn.close()
    actualizar_lista_envios()
    messagebox.showinfo("Éxito", "Estado del envío actualizado correctamente")

# Interfaz gráfica
root = tk.Tk()
root.title("Gestión de Envíos")

# Entradas de datos
tk.Label(root, text="Número de Seguimiento").grid(row=0, column=0)
entry_numero_seguimiento = tk.Entry(root)
entry_numero_seguimiento.grid(row=0, column=1)

tk.Label(root, text="Origen").grid(row=1, column=0)
entry_origen = tk.Entry(root)
entry_origen.grid(row=1, column=1)

tk.Label(root, text="Destino").grid(row=2, column=0)
entry_destino = tk.Entry(root)
entry_destino.grid(row=2, column=1)

tk.Label(root, text="Fecha de Entrega Prevista").grid(row=3, column=0)
entry_fecha_entrega_prevista = tk.Entry(root)
entry_fecha_entrega_prevista.grid(row=3, column=1)

tk.Button(root, text="Agregar Envío", command=agregar_envio).grid(row=4, column=0, columnspan=2)

# Lista de envíos
columns = ("ID", "Número de Seguimiento", "Origen", "Destino", "Fecha de Entrega Prevista", "Estado")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=4)

# Actualización de estado
tk.Label(root, text="Nuevo Estado").grid(row=6, column=0)
combo_estado = ttk.Combobox(root, values=["En tránsito", "Entregado"])
combo_estado.grid(row=6, column=1)
tk.Button(root, text="Actualizar Estado", command=actualizar_envio).grid(row=6, column=2)

# Inicializar lista de envíos
actualizar_lista_envios()

root.mainloop()
