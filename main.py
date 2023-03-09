import tkinter as tk
from tkinter import ttk
import psycopg2
import datetime
from PIL import Image, ImageTk

MAIN_BG_COLOR = "#f4b042"

class UserProfile(tk.Toplevel):
    def __init__(self, user_data):
        super().__init__()
        self.config(bg=MAIN_BG_COLOR)
        self.title("Perfil de usuario")

        # Mostrar la información del usuario en etiquetas
        name_label = tk.Label(self, text=f"Usuario: {user_data[1]}")
        name_label.pack()

        email_label = tk.Label(self, text=f"Edad: {user_data[4]}")
        email_label.pack()

        email_label = tk.Label(self, text=f"Peso: {user_data[5]}")
        email_label.pack()
        
        email_label = tk.Label(self, text=f"Altura: {user_data[6]}")
        email_label.pack()

        email_label = tk.Label(self, text=f"Actividad Fisica: {user_data[7]}")
        email_label.pack()

        # Mostrar la imagen del avatar
        avatar_image = tk.PhotoImage(file="avatar.png")
        avatar_label = tk.Label(self, image=avatar_image)
        avatar_label.image = avatar_image
        avatar_label.pack()
       
        # Agregar botón de Recetas
        recetas_button = tk.Button(self, text="Recetas", command=self.show_recipes)
        recetas_button.pack()

    def show_recipes(self):
        # Cargar contenido de recetas desde otro archivo
        import recetas
        recetas_text = recetas.load_recipes()
        recetas_label = tk.Label(recetas_window, text=recetas_text)
        recetas_label.pack()

class NutriappLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("400x600")
        self.root.config(bg="#f4b042")

        # Cargar la imagen y crear el objeto tk.PhotoImage
        image = Image.open("titulo.png")
        self.photo = ImageTk.PhotoImage(image)

        # Crear el widget tk.Label y configurar la imagen
        title_label = tk.Label(self.root, image=self.photo, bg="#f4b042")
        title_label.pack(pady=20)

        # Crear el campo de entrada para el usuario
        username_label = tk.Label(self.root, text="Usuario:", bg='#c38c34', fg='#ffffff')
        username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        # Crear el campo de entrada para la contraseña
        password_label = tk.Label(self.root, text="Contraseña:", bg='#c38c34', fg='#ffffff')
        password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        # Crear los botones de ingreso y crear usuario
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        login_button = tk.Button(button_frame, text="Ingresar", command=self.show_profile, bg='#c38c34', fg='#ffffff')
        login_button.pack(side=tk.LEFT, padx=5)

        create_button = tk.Button(button_frame, text="Crear", command=self.create_user, bg='#c38c34', fg='#ffffff')
        create_button.pack(side=tk.LEFT, padx=5)

    def create_user(self):
        def calculate_bmi():
            global bmi
            weight = float(weight_entry.get())
            height = float(height_entry.get())/100
            bmi = round(weight / (height * height), 2)
            bmi_label.config(text=f"BMI: {bmi}")

        def calculate_bmr():
            global bmr
            weight = float(weight_entry.get())
            height = float(height_entry.get())
            age = int(age_entry.get())
            activity_level = activity_var.get()

            if gender_var.get() == "Male":
                bmr = round((10 * weight) + (6.25 * height) - (5 * age) + 5, 2)
            else:
                bmr = round((10 * weight) + (6.25 * height) - (5 * age) - 161, 2)

            if activity_level == "Sedentario":
                bmr *= 1.2
            elif activity_level == "Poco activo":
                bmr *= 1.375
            elif activity_level == "Moderadamente activo":
                bmr *= 1.55
            elif activity_level == "Activo":
                bmr *= 1.725
            else:
                bmr *= 1.9

            bmr_label.config(text=f"BMR: {bmr}")

        def calculate():
            if user_entry.get() == "" or password_entry.get() == "" or name_entry.get() == "" or age_entry.get() == "" or weight_entry.get() == "" or height_entry.get() == "":
                bmi_label.config(text="Por favor complete todos los campos.")
                bmr_label.config(text="")
            else:
                calculate_bmi()
                calculate_bmr()

                # Conectarse a la base de datos
                conn = psycopg2.connect(
                    user="postgres",
                    password="homero",
                    database="Nutriapp"
                )

                # Crear un cursor
                cursor = conn.cursor()

                # Obtener el ID correspondiente al nivel de actividad seleccionado
                sql = "SELECT id_actividad FROM nivel_actividad WHERE tipo_actividad = %s"
                val = (activity_var.get(),)
                cursor.execute(sql, val)
                nivel_actividad_id = cursor.fetchone()[0]

                # Insertar datos en la tabla usuarios
                sql = "INSERT INTO usuarios (nombre_usuario, password, nombre_completo, edad, peso, altura, nivel_actividad, genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (user_entry.get(), password_entry.get(), name_entry.get(), int(age_entry.get()), float(weight_entry.get()), float(height_entry.get()), nivel_actividad_id, gender_var.get())
                cursor.execute(sql, val)

                # Obtener el id del nuevo usuario
                sql = "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s"
                val = (user_entry.get(),)
                cursor.execute(sql, val)
                id_usuario = cursor.fetchone()[0]

                # Insertar datos en la tabla progreso
                sql = "INSERT INTO progreso (id_usuario, fecha_efectiva, imc, bmr) VALUES (%s, %s, %s, %s)"
                val = (id_usuario, datetime.date.today(), float(bmi), float(bmr))
                cursor.execute(sql, val)

                # Mostrar mensaje de éxito
                from tkinter import messagebox
                messagebox.showinfo("Éxito", "La cuenta ha sido creada exitosamente, puede ingresar")

                # Crear una nueva instancia de la clase UserProfile con los datos del nuevo usuario
                root.destroy()

                # Guardar los cambios y cerrar la conexión
                conn.commit()
                cursor.close()
                conn.close()

        root = tk.Tk()
        root.config(bg=MAIN_BG_COLOR)
        root.geometry("400x600")
        root.title("Calculadora de IMC y BMR")
      
        style = ttk.Style()

        gender_var = tk.StringVar(value="Masculino")
        activity_var = tk.StringVar(value="Sedentario")

        user_label = ttk.Label(root, text="Usuario:", background='#c38c34',foreground="#FFFFFF")
        user_label.grid(column=0, row=0, padx=5, pady=5)

        user_entry = ttk.Entry(root)
        user_entry.grid(column=1, row=0, padx=5, pady=5)

        password_label = ttk.Label(root, text="Contraseña:", background='#c38c34',foreground="#FFFFFF")
        password_label.grid(column=0, row=1, padx=5, pady=5)

        password_entry = ttk.Entry(root, show="*")
        password_entry.grid(column=1, row=1, padx=5, pady=5)

        name_label = ttk.Label(root, text="Nombre completo:", background='#c38c34',foreground="#FFFFFF")
        name_label.grid(column=0, row=2, padx=5, pady=5)

        name_entry = ttk.Entry(root)
        name_entry.grid(column=1, row=2, padx=5, pady=5)

        age_label = ttk.Label(root, text="Edad:", background='#c38c34',foreground="#FFFFFF")
        age_label.grid(column=0, row=3, padx=5, pady=5)

        age_entry = ttk.Entry(root)
        age_entry.grid(column=1, row=3, padx=5, pady=5)

        weight_label = ttk.Label(root, text="Peso (kg):", background='#c38c34',foreground="#FFFFFF")
        weight_label.grid(column=0, row=4, padx=5, pady=5)

        weight_entry = ttk.Entry(root)
        weight_entry.grid(column=1, row=4, padx=5, pady=5)

        height_label = ttk.Label(root, text="Altura (cm):", background='#c38c34',foreground="#FFFFFF")
        height_label.grid(column=0, row=5, padx=5, pady=5)

        height_entry = ttk.Entry(root)
        height_entry.grid(column=1, row=5, padx=5, pady=5)

        activity_label = ttk.Label(root, text="Nivel de actividad física:", background='#c38c34',foreground="#FFFFFF")
        activity_label.grid(column=0, row=6, padx=5, pady=5)

        activity_combobox = ttk.Combobox(root,textvariable=activity_var, values=["Sedentario", "Poco activo", "Moderadamente activo", "Activo", "Muy activo"], background='#c38c34',foreground="#FFFFFF")
        activity_combobox.grid(column=1, row=6, padx=5, pady=5)

        gender_label = ttk.Label(root, text="Género:")
        gender_label.grid(column=0, row=7, padx=5, pady=5)

        male_radio = ttk.Radiobutton(root, text="Masculino", variable=gender_var, value="Masculino")
        male_radio.grid(column=1, row=7, padx=5, pady=5)

        female_radio = ttk.Radiobutton(root, text="Femenino", variable=gender_var, value="Femenino")
        female_radio.grid(column=2, row=7, padx=5, pady=5)

        calculate_button = ttk.Button(root, text="Crear Usuario", command=calculate)
        calculate_button.grid(column=0, row=8, padx=5, pady=5,)

        bmi_label = ttk.Label(root, text="")
        bmi_label.grid(column=0, row=9, padx=5, pady=5)

        bmr_label = ttk.Label(root, text="")
        bmr_label.grid(column=0, row=10, padx=5, pady=5)

    def run(self):
        self.root.mainloop()

    def show_profile(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Conectar a la base de datos
            conn = psycopg2.connect(
                database="Nutriapp",
                user="postgres",
                password="homero"
            )

            # Crear un cursor para ejecutar las consultas
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario=%s", (username,))
            user_data = cursor.fetchone()

            if user_data:
                # Verificar si la contraseña coincide
                if user_data[2] == password:
                    # Mostrar la ventana de perfil del usuario
                    profile = UserProfile(user_data)
                    profile.geometry("400x600") # Agregar esta líne
                    profile.grab_set()
                else:
                    print("Contraseña incorrecta")
            else:
                print("El usuario no existe")

            # Cerrar el cursor y la conexión a la base de datos
            cursor.close()
            conn.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

if __name__ == '__main__':
    app = NutriappLogin()
    app.run()
