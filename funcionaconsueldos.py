import os
import sys
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image


def obtener_ruta_tesseract():
    if getattr(sys, 'frozen', False):  
        carpeta_temporal = os.path.dirname(sys.executable)  
        tesseract_path = os.path.join(carpeta_temporal, 'tesseract-ocr', 'tesseract.exe')  
    else:  
        tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract-ocr', 'tesseract.exe')  

    return tesseract_path

pytesseract.pytesseract.tesseract_cmd = obtener_ruta_tesseract()

def extraer_texto_ocr(imagen):
    texto_ocr = pytesseract.image_to_string(imagen)
    return texto_ocr

def buscar_rut(texto):
    match = re.search(r'(?<=Rut[:\s])(\d{7,8}-[Kk0-9])', texto)
    if match:
        return match.group(1)
    return None

def limpiar_texto(texto):
    texto_limpio = " ".join(texto.split())
    return texto_limpio

def separar_sueldos(pdf_path, output_dir):
    documento = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(documento)):
        pagina = documento[i]
        
        texto = pagina.get_text("text")
        texto_limpio = limpiar_texto(texto)  

        if texto_limpio:
            rut = buscar_rut(texto_limpio)
            if rut:
                nuevo_pdf = fitz.open()
                nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
                output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")  
                nuevo_pdf.save(output_pdf_path)
                continue  

        pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2)) 
        imagen = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        texto_ocr = extraer_texto_ocr(imagen)
        texto_ocr_limpio = limpiar_texto(texto_ocr)  

        rut = buscar_rut(texto_ocr_limpio)
        if rut:
            nuevo_pdf = fitz.open()
            nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
            output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")  
            nuevo_pdf.save(output_pdf_path)

    return output_dir
