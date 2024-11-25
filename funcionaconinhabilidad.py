import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tesseract-OCR", "tesseract.exe")

def extraer_texto_ocr(imagen):
    texto_ocr = pytesseract.image_to_string(imagen)
    print(f"Texto OCR extraído: {texto_ocr}")  
    return texto_ocr

def normalizar_texto(texto):
    texto_normalizado = texto.replace("Cién", "Ción")  
    texto_normalizado = re.sub(r'\s+', ' ', texto_normalizado) 
    texto_normalizado = re.sub(r'[^\w\s-]', '', texto_normalizado)  
    return texto_normalizado.strip()  

def buscar_rut(texto):
    print(f"Texto para buscar RUT: {texto}")
    match = re.search(r'\b(RUN|RUT)[\s:]*([\d]{7,8})-?([0-9Kk])\b', texto)
    if match:
        return f"{match.group(2)}-{match.group(3)}"
    return None



def limpiar_texto(texto):
    texto_limpio = normalizar_texto(texto)
    return texto_limpio

def separar_paginas_con_rut(pdf_path):
    documento = fitz.open(pdf_path)
    nombre_archivo = os.path.splitext(os.path.basename(pdf_path))[0]
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_pdfs")
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(documento)):
        pagina = documento[i]
        
        texto = pagina.get_text("text")
        texto_limpio = limpiar_texto(texto) 

        if texto_limpio:
            print(f"Texto extraído de la página {i+1}: {texto_limpio}") 
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
        texto_ocr_limpio = limpiar_texto(texto_ocr)  
        print(f"Texto OCR limpio: {texto_ocr_limpio}") 

        rut = buscar_rut(texto_ocr_limpio)
        if rut:
            print(f"RUT encontrado con OCR en la página {i+1}: {rut}")
            nuevo_pdf = fitz.open()
            nuevo_pdf.insert_pdf(documento, from_page=i, to_page=i)
            output_pdf_path = os.path.join(output_dir, f"{rut}.pdf")
            nuevo_pdf.save(output_pdf_path)
            print(f"Se guardó el PDF con RUT {rut} en: {output_pdf_path}")
        else:
            print(f"No se encontró RUT en la página {i+1} ni con OCR.")

    
pdf_path = r"inhabilidad.pdf" 
separar_paginas_con_rut(pdf_path)
