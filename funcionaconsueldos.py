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

def separar_sueldos(pdf_path, output_dir):
    documento = fitz.open(pdf_path)
    
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

        print(f"No se encontró RUT en la página {i+1} desde texto, usando OCR")

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
    
    return output_dir

