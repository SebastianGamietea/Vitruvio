import tkinter as tk
from tkinter import ttk
import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    database="Nutriapp",
    user="postgres",
    password="homero"
)

# Crear cursor
cur = conn.cursor()

# Crear ventana de tkinter
root = tk.Tk()
root.geometry("400x600")

# Crear contenedor para el cuadro de texto y la barra de desplazamiento
container = ttk.Frame(root)
container.pack(fill=tk.BOTH, expand=True)

# Crear barra de desplazamiento
scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear cuadro de texto para mostrar los datos
text_box = tk.Text(container, wrap='word', yscrollcommand=scrollbar.set)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configurar la barra de desplazamiento para que se ajuste al cuadro de texto
scrollbar.config(command=text_box.yview)

# Ejecutar consulta SELECT a la tabla Recetas
cur.execute("SELECT id_receta, nombre, descripción, string_agg(instrucciones, '\n') FROM Recetas GROUP BY id_receta")

# Mostrar los resultados en el cuadro de texto
for row in cur:
    text_box.insert(tk.END, f"Nombre: {row[1]}\n")
    text_box.insert(tk.END, f"Descripción: {row[2]}\n")
    text_box.insert(tk.END, f"Instrucciones:\n{row[3]}\n\n")

# Cerrar cursor y conexión
cur.close()
conn.close()

# Iniciar la aplicación de tkinter
root.mainloop()
