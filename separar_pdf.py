# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
# 1. separar las paginas del pdf y hacer un pdf por paginas / listo
# 2. que el nombre de cada pdf sea el rut  / listo 
# 2.1 funciona en diferentes archivos pero por separado, hay que hacerlo en un solo archivo py 
# 3- empesar app
# 4 detalles
# 4.1. opcion de cambiar el nombre del pdf a xx.xxx.xxx-cer o xx.xxx.xxx-x
# 4.2 selector de archivos
# 4.3 añadir opcion para el nombre, que termine en cer o con el digito verificador
## verificari si el rut tiene puntos, ti tiene puntos se quitan
## agregar el selector de archivos
#agregar 2 opciones para los tipo de documento, certificado o sueldo,
# si es certificado se debe guardar el nombre xx.xxx.xxx-cer y si es sueldo se va a guardar xx.xxx.xxx-x
# la app tendra 3 scripts 1 separar_pdf.py que sera el archivo principal, contara con la interfaz, la logica es que aqui el usuario marcara
# del tipo de documento y seleccionara los archivos.
#el segundo scrirpt es funcion_cer.py que su logica es para los certificados de inhabilidad
# el tecer script es funcion_sueldo.py que servira para los sueldos

"""
La app de escritorio

al abrir la app se vera el nombre procesador de pdf, abajo estara una seleccion de opciones, para selecionar el tipo de documento
y debajo de esto estara el boton de seleccionar archivo, ahi se seleccionara el pdf o los pdf que necesite procesar, 
segun el tipo de archivo que se seleccione se usara funcion_cer.py o funcion_sueldos.py para procesar el pdf, 
al finalizar el proceso se creara una carpeta con los pdf, esta carpeta se descargara y elegira la ubicacion donde se desea guardar
si se procesa bien el pdf saldra un mensaje que diga "se proceso correctamente" y en caso de algun error dira"no se pudo procesar el pdf"
"""
import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  

def extraer_texto_ocr(imagen):
    texto_ocr = pytesseract.image_to_string(imagen)
    return texto_ocr

def buscar_rut(texto):
    match = re.search(r'(?<=Rut[:\s])(\d{7,8}-[Kk0-9])', texto)
    if match:
        return match.group(1)
    return None

def separar_paginas_con_rut(pdf_path):
    documento = fitz.open(pdf_path)
    nombre_archivo = os.path.splitext(os.path.basename(pdf_path))[0]
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_pdfs")
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(documento)):
        pagina = documento[i]
        
        texto = pagina.get_text("text")
        texto_limpio = " ".join(texto.split())  

        if texto_limpio:
       
            rut = buscar_rut(texto_limpio)
            if rut:
                print(f"RUT encontrado en la página {i+1} desde texto: {rut}")
                nuevo_pdf = fitz.open()
                nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
                output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")
                nuevo_pdf.save(output_pdf_path)
                print(f"Se guardó el PDF con RUT {rut} en: {output_pdf_path}")
                continue  

        print(f"No se encontró RUT en la página {i+1} desde texto, usando OCR...")

        pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))  
        imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        texto_ocr = extraer_texto_ocr(imagen)
        print(f"Texto OCR extraído de la página {i+1}: {texto_ocr}")

        rut = buscar_rut(texto_ocr)
        if rut:
            print(f"RUT encontrado con OCR en la página {i+1}: {rut}")
            nuevo_pdf = fitz.open()
            nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
            output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")
            nuevo_pdf.save(output_pdf_path)
            print(f"Se guardó el PDF con RUT {rut} en: {output_pdf_path}")
        else:
            print(f"No se encontró RUT en la página {i+1} ni con OCR.")


pdf_path = r"sueldos.pdf" 
separar_paginas_con_rut(pdf_path)
