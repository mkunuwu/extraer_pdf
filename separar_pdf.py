# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
# 1. separar las paginas del pdf y hacer un pdf por paginas / listo
# 2. que el nombre de cada pdf sea el rut  / listo 
# 2.1 funciona en diferentes archivos pero por separado, hay que hacerlo en un solo archivo py 
# 3- empesar app
# 4 detalles
# 4.1. opcion de elegir el tipo de archivo, si es sueldos o inhabilidad 
# 4.2 selector de archivos
# 4.3 añadir opcion para el nombre, que termine en cer si es inhabilidad o con el digito verificador si es sueldo listo
# 5 empezar interfaz de usuario
# 5.1 agregar selector de archivos en interfaz listo
# 5.2 agregar seleccion de tipo de archivo
#  verificari si el rut tiene puntos, ti tiene puntos se quitan listo
#  agregar el selector de archivos LISTO
# la app tendra 3 scripts 1 separar_pdf.py que sera el archivo principal, contara con la interfaz, 
# la logica es que aqui el usuario marcara
# el tipo de documento y seleccionara los archivos.
#el segundo scrirpt es funcion_cer.py que su logica es para los certificados de inhabilidad
# el tecer script es funcion_sueldo.py que servira para los sueldos
#e
"""
La app de escritorio

al abrir la app se vera el nombre procesador de pdf, abajo estara una seleccion de opciones, para selecionar el tipo de documento
y debajo de esto estara el boton de seleccionar archivo, ahi se seleccionara el pdf o los pdf que necesite procesar, 
segun el tipo de archivo que se seleccione se usara funcion_cer.py o funcion_sueldos.py para procesar el pdf, 
al finalizar el proceso se creara una carpeta con los pdf, esta carpeta se descargara y elegira la ubicacion donde se desea guardar
si se procesa bien el pdf saldra un mensaje que diga "se proceso correctamente" y en caso de algun error dira"no se pudo procesar el pdf"
"""
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo PDF", 
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    if archivo:  
        etiqueta_archivo.config(text=f"Archivo seleccionado: {archivo}")
    else:
        etiqueta_archivo.config(text="No se seleccionó ningún archivo")

root = tk.Tk()
root.title("Seleccionador de Archivos PDF")  
root.geometry("400x200") 

boton_seleccionar = tk.Button(
    root, 
    text="Seleccionar archivo PDF", 
    command=seleccionar_archivo, 
    width=30, 
    height=2
)
boton_seleccionar.pack(pady=20)

etiqueta_archivo = tk.Label(root, text="No se ha seleccionado ningún archivo", wraplength=350)
etiqueta_archivo.pack(pady=10)

root.mainloop()
