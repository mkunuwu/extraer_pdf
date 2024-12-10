import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tesseract-OCR", "tesseract.exe")

def extraer_texto_ocr(imagen):
    texto_ocr = pytesseract.image_to_string(imagen)
    return texto_ocr

def normalizar_texto(texto):
    texto_normalizado = texto.replace("Cién", "Ción")  
    texto_normalizado = re.sub(r'\s+', ' ', texto_normalizado) 
    texto_normalizado = re.sub(r'[^\w\s-]', '', texto_normalizado)  
    return texto_normalizado.strip()  

def buscar_rut(texto):
    match = re.search(r'\b(RUN|RUT)[\s:]*([\d]{7,8})-?([0-9Kk])\b', texto)
    if match:
        rut_base = f"{match.group(2)}-{match.group(3)}"
        rut_modificado = f"{match.group(2)}-cer"
        return rut_modificado  
    return None

def limpiar_texto(texto):
    texto_limpio = normalizar_texto(texto)
    return texto_limpio

def separar_inhabilidades(pdf_path, output_dir):
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
