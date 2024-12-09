# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
# 1. separar las paginas del pdf y hacer un pdf por paginas / listo
# 2. que el nombre de cada pdf sea el rut  / listo 
# 2.1 funciona en diferentes archivos pero por separado, hay que hacerlo en un solo archivo py 
# 3- empesar app
# 4 detalles
# 4.1. opcion de elegir el tipo de archivo, si es sueldos o inhabilidad listo
# 4.2 selector de archivos
# 4.3 añadir opcion para el nombre, que termine en cer si es inhabilidad o con el digito verificador si es sueldo listo
# 5 empezar interfaz de usuario 
# 5.1 agregar selector de archivos en interfaz listo
# 5.2 agregar seleccion de tipo de archivo listo
#  verificari si el rut tiene puntos, ti tiene puntos se quitan listo
#  agregar el selector de archivos LISTO
# la app tendra 3 scripts 1 separar_pdf.py que sera el archivo principal, contara con la interfaz, 
# la logica es que aqui el usuario marcara
# el tipo de documento y seleccionara los archivos. listo
#el segundo scrirpt es funcion_cer.py que su logica es para los certificados de inhabilidad
# el tecer script es funcion_sueldo.py que servira para los sueldos
# no se pudo procesar el archivo: separar_inhabilidades() missing 1 required positional argument 'output_dir'
# agregar barra o circulo de carga
# agregar que se pueda procesar mas de un pdf
#agregar diseño mas atractivo
# hacer documentacion
# Se queda guardado los pdf en la carpeta temporal solucionado
# cuando no puede procesar, dice proceso exitoso SOLUCIONADO 

"""
La app de escritorio
al abrir la app se vera el nombre procesador de pdf, abajo estara una seleccion de opciones, para selecionar el tipo de documento
y debajo de esto estara el boton de seleccionar archivo, ahi se seleccionara el pdf o los pdf que necesite procesar, 
segun el tipo de archivo que se seleccione se usara funcionaconinhabilidad.py o funcionconsueldos.py para procesar el pdf, 
al finalizar el proceso se creara una carpeta con los pdf, esta carpeta se descargara y elegira la ubicacion donde se desea guardar
si se procesa bien el pdf saldra un mensaje que diga "se proceso correctamente" y en caso de algun error dira"no se pudo procesar el pdf"
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from funcionaconsueldos import separar_sueldos  
from funcionaconinhabilidad import separar_inhabilidades
import threading

output_dir = None
temp_output_dir = "temp_output_pdfs"

def vaciar_carpeta_temporal():
    if os.path.exists(temp_output_dir):
        for archivo in os.listdir(temp_output_dir):
            archivo_path = os.path.join(temp_output_dir, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)

def seleccionar_archivo():
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivos PDF", 
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    archivos = list(archivos)  
    
    if archivos:  
        etiqueta_archivo.config(text=f"Archivos seleccionados: {', '.join(archivos)}")
        procesar_archivos(archivos)  
    else:
        etiqueta_archivo.config(text="No se seleccionaron archivos")


def procesar_archivos(archivos):
    global output_dir 
    
    tipo_documento = tipo_documento_var.get()
    
    if tipo_documento == "Seleccionar tipo":
        messagebox.showerror("Error", "Selecciona el tipo de documento (Sueldos o Inhabilidad)")
        return

    output_dir = os.path.join(os.getcwd(), temp_output_dir)
    
    vaciar_carpeta_temporal()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def procesar_siguiente_archivo():
        if archivos:
            archivo = archivos.pop(0)
            try:
                if tipo_documento == "Sueldos":
                    separar_sueldos(archivo, output_dir)  
                
                elif tipo_documento == "Inhabilidad":
                    separar_inhabilidades(archivo, output_dir)  

                if not os.listdir(output_dir):
                    messagebox.showerror("Error", "No se pudieron procesar los PDFs. Asegúrese de que el archivo es válido para el tipo seleccionado.")
                else:
                    messagebox.showinfo("Éxito", f"El PDF {archivo} fue procesado correctamente.")
                    boton_descargar.config(state=tk.NORMAL)  
                    etiqueta_archivo.config(text=f"PDF procesado: {archivo}")

                procesar_siguiente_archivo()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo {archivo}: {e}")
        else:
            messagebox.showinfo("Éxito", "Todos los archivos han sido procesados.")

    procesar_siguiente_archivo()

def descargar_carpeta():
    if output_dir:
        carpeta_destino = filedialog.asksaveasfilename(
            defaultextension="",
            filetypes=[("Carpeta", "")],
            title="Seleccionar ubicación para guardar la carpeta",
            initialdir=os.getcwd()
        )
        
        if carpeta_destino:
            nombre_carpeta = os.path.basename(carpeta_destino)  
            
            if nombre_carpeta == "":
                nombre_carpeta = "ArchivosProcesados"
            
            carpeta_final = os.path.join(os.path.dirname(carpeta_destino), nombre_carpeta)
            
            if not os.path.exists(carpeta_final):
                os.makedirs(carpeta_final)
            
            try:
                for archivo in os.listdir(output_dir):
                    archivo_origen = os.path.join(output_dir, archivo)
                    archivo_destino = os.path.join(carpeta_final, archivo)
                    shutil.copy(archivo_origen, archivo_destino)

                messagebox.showinfo("Éxito", f"La carpeta se ha descargado en: {carpeta_final}")
                
               # shutil.rmtree(output_dir)
              #  messagebox.showinfo("Éxito", "La carpeta temporal ha sido eliminada.")
            except Exception as e:
                messagebox.showerror("Error:", f"{e}")
    else:
        messagebox.showerror("Error", "No se ha procesado ningún archivo aún.")

root = tk.Tk()
root.title("Procesador de PDF")  
root.geometry("500x350") 

tipo_documento_var = tk.StringVar(value="Seleccionar tipo")
etiqueta_tipo_documento = tk.Label(root, text="Seleccionar tipo de documento:")
etiqueta_tipo_documento.pack(pady=5)

opciones_tipo_documento = ["Sueldos", "Inhabilidad"]
menu_tipo_documento = tk.OptionMenu(root, tipo_documento_var, *opciones_tipo_documento)
menu_tipo_documento.pack(pady=5)

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

boton_descargar = tk.Button(
    root,
    text="Descargar carpeta",
    command=descargar_carpeta,
    width=30,
    height=2,
    state=tk.DISABLED  
)
boton_descargar.pack(pady=20)

root.mainloop()
