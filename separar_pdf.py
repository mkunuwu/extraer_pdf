# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
# 1. separar las paginas del pdf y hacer un pdf por paginas
# 2. que el nombre de cada pdf sea el rut 
# 3- empesar app
# 4. opcion de cambiar el nombre del pdf a xx.xxx.xxx-cer o xx.xxx.xxx-x
## verificari si el rut tiene puntos, ti tiene puntos se quitan
## agregar el selector de archivos
import os
import re
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'  # Cambia esta ruta si es necesario


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
        print(f"Texto extraído de la página {i+1}: {texto}")
        
        texto_limpio = " ".join(texto.split())
        print(f"Texto limpiado de la página {i+1}: {texto_limpio}")
        
        rut = buscar_rut(texto_limpio)
        
        if rut:
            print(f"RUT encontrado: {rut}")

            nuevo_pdf = fitz.open()
            nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
            
            output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")
            
            nuevo_pdf.save(output_pdf_path)
            print(f"Se guardó el PDF en: {output_pdf_path}")
            
        else:
            print(f"No se encontró un RUT en la página {i+1}, usando OCR...")
            imagen = convert_from_path(pdf_path, first_page=i+1, last_page=i+1)[0]
            texto_ocr = extraer_texto_ocr(imagen)
            print(f"Texto OCR extraído de la página {i+1}: {texto_ocr}")
            
            rut = buscar_rut(texto_ocr)
            
            if rut:
                print(f"RUT encontrado con OCR: {rut}")
                nuevo_pdf = fitz.open()
                nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
                
                output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")
                
                nuevo_pdf.save(output_pdf_path)
                print(f"Se guardó el PDF en: {output_pdf_path}")
            else:
                print(f"No se encontró RUT en la página {i+1} ni con OCR.")


pdf_path = r"sueldos.pdf"  
separar_paginas_con_rut(pdf_path)
