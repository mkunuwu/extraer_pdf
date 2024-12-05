import os
import re
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tesseract-OCR", "tesseract.exe")

def extraer_texto_ocr(imagen):
    texto_ocr = pytesseract.image_to_string(imagen)
    print(f"Texto OCR extraído: {texto_ocr}")  
    return texto_ocr

def buscar_rut(texto):
    print(f"Texto para buscar RUT: {texto}")
    # Asegúrate de que la expresión regular cubra todos los casos posibles
    match = re.search(r'(?<=Rut[:\s])(\d{7,8}-[Kk0-9])', texto)
    if match:
        return match.group(1)
    return None

def limpiar_texto(texto):
    # Elimina caracteres innecesarios, pero no toques demasiado el texto
    texto_limpio = " ".join(texto.split())  # Solo reemplaza saltos de línea y espacios extra
    return texto_limpio

def separar_sueldos(pdf_path, output_dir):
    documento = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(documento)):
        pagina = documento[i]
        
        texto = pagina.get_text("text")
        texto_limpio = limpiar_texto(texto)  # Solo limpia el texto, no lo normalices tanto

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

        pix = pagina.get_pixmap(matrix=fitz.Matrix(2, 2))  # Convierte la página en imagen
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

    return output_dir
