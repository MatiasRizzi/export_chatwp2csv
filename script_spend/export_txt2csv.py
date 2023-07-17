import tkinter as tk
from tkinter import filedialog,  messagebox
import pandas as pd
from datetime import datetime 



def open_file(month, year):
    # Abrir el diálogo de selección de archivo
    archivo = filedialog.askopenfilename(filetypes=[("Archivos txt", "*.txt")])

    if archivo:
        # Leer el archivo CSV utilizando pandas
        df = red_file(archivo,year, month)
        
        # Mostrar los datos en la consola (puedes modificar esto según tus necesidades)
        guardar_archivo(df)
        print(df)

def guardar_archivo(df):
    archivo_guardado = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])

    """ if archivo_guardado:
        df.to_csv(archivo_guardado, index=False)
        print("Archivo guardado correctamente.") """
    
    if archivo_guardado:
        try:
            df.to_csv(archivo_guardado, index=False)
            messagebox.showinfo("Éxito", "El archivo se guardó correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")

def red_file(filename, year, month):
    # Leer el archivo de texto
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    #Example line
    # 6/3/23, 22:44 - Barby: 4200 torta

    # Eliminar las líneas de información del chat que no son necesarias
    lines = [line for line in lines if not (line.startswith('[') or line.startswith('Mensajes'))]

    # Validar que la linea comienza con una fecha y con el formato de fecha
    lines_with_dates = []
    format = "%d/%m/%y"
    for line in lines:
        if line:
            try:
                timestamp, message = line.split(', ', 1)
                datetime.strptime(timestamp, format)
                lines_with_dates.append(line)
            except ValueError:
                continue

    # eliminar las lineas que no corresponden a la fecha ingresada
    lines_of_month =  []
    for line in lines_with_dates:
        timestamp, message = line.split(', ', 1)
        date_dt = datetime.strptime(timestamp, '%m/%d/%y')
        if  date_dt.month == int(month) and (date_dt.year == int(year) or date_dt.year == int(f'20{year}') ) :
            lines_of_month.append(line)
    # Improvement: Crear una lista de mensajes, donde cada mensaje es una lista de [remintente, mensaje]

    messages = []
    for line in lines_of_month:
        if line.startswith('\n'):
            continue
        else:
            line = line.strip()
            #TODO try catch para separar tiempo y mensaje y ademas que mensaje empieze con Barby o matias, sino descarta la linea
            timestamp, message = line.split(': ')
            date_str, sender = timestamp.split(' - ')

            #date = datetime.strptime(date_str, '%m/%d/%y, %H:%M')
            #if date.month == month:
            #TODO es posible cambiar el split por espacio, pero hay que pensar como unir varias palabras en la descripcion
            try:
                amount, description = message.split(' ', 1)
            except ValueError:
                print("Fail format text")
                continue

            
            #TODO sacar espacio y signo peso al monto si es que lo tiene
            if '$' in amount:
                _, amount = amount.split('$')
            messages.append([sender, description, amount])

    # Crear un DataFrame de pandas a partir de la lista de mensajes
    df = pd.DataFrame(messages, columns=['Remitente', 'Mensaje', 'Monto'])
    #path=r'C:\Users\Usuario\OneDrive\Documentos\Python'
    # Exportar el DataFrame como un archivo CSV
    #import pdb; pdb.set_trace()
    #df.to_csv(path+f'\\gastos_mes_{month}.csv', index=False)
    return df


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Export file from whatsapp")

# Establecer las dimensiones de la ventana
ventana.geometry("400x300")  # Ancho x Alto

# Variables para almacenar los valores de mes y año
mes_var = tk.StringVar()
anio_var = tk.StringVar()

# Función para obtener los valores ingresados y llamar a abrir_archivo
def abrir_archivo_wrapper():
    mes = mes_var.get()
    anio = anio_var.get()
    open_file(mes, anio)

# Crear etiqueta y cuadro de entrada para el mes
etiqueta_mes = tk.Label(ventana, text="Mes:")
etiqueta_mes.pack()
entrada_mes = tk.Entry(ventana, textvariable=mes_var)
entrada_mes.pack()

# Crear etiqueta y cuadro de entrada para el año
etiqueta_anio = tk.Label(ventana, text="Año:")
etiqueta_anio.pack()
entrada_anio = tk.Entry(ventana, textvariable=anio_var)
entrada_anio.pack()


# Botón para abrir el archivo CSV
boton_abrir = tk.Button(ventana, text="Open wp file ", command=abrir_archivo_wrapper)
boton_abrir.pack()

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
