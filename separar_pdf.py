# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
# 1. separar las paginas del pdf y hacer un pdf por paginas
# 2. que el nombre de cada pdf sea el rut 
# 3- empesar app
# 4. opcion de cambiar el nombre del pdf a xx.xxx.xxx-cer o xx.xxx.xxx-x
## verificari si el rut tiene puntos, ti tiene puntos se quitan
## agregar el selector de archivos
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import io

pytesseract.pytesseract.tesseract_cmd = r'"C:\Users\practicante.ti\AppData\Local\Programs\Tesseract-OCR"'  # Cambia la ruta si es necesario

def extraer_rut(texto):
    rut_pattern = r'(?i)rut\s*[:;]?\s*(\d{1,2}\.\d{3}\.\d{3}-[\dkK])'
    match = re.search(rut_pattern, texto)
    if match:
        return match.group(1) 
    return None

def extraer_texto_pdf(doc, page_number):
    page = doc.load_page(page_number) 
    return page.get_text("text")  

def extraer_texto_ocr(imagen):
    return pytesseract.image_to_string(imagen)

def extraer_imagen_de_pagina(doc, page_number):
    page = doc.load_page(page_number)
    image_list = page.get_images(full=True)
    
    if image_list:
        xref = image_list[0][0] 
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"] 
        image = Image.open(io.BytesIO(image_bytes)) 
        return image
    return None 

def separar_paginas_con_rut(pdf_path):

    doc = fitz.open(pdf_path)
    num_paginas = doc.page_count
    
    for i in range(num_paginas):
        texto = extraer_texto_pdf(doc, i)
        
        print(f"Texto de la página {i + 1}:")
        print(texto) 
        
        if texto.strip():
            rut = extraer_rut(texto)
        else:
            print(f"Usando OCR en la página {i + 1}...")
            imagen = extraer_imagen_de_pagina(doc, i)
            
            if imagen:
                texto_ocr = extraer_texto_ocr(imagen)
                print(f"Texto OCR de la página {i + 1}:")
                print(texto_ocr) 
                rut = extraer_rut(texto_ocr)
            else:
                rut = None

        if rut:
            pdf_writer = fitz.open() 
            pagina = doc.load_page(i)
            pdf_writer.insert_pdf(doc, from_page=i, to_page=i)
            
            nombre_pdf = f"{rut}.pdf"
            pdf_writer.save(nombre_pdf)
            print(f"Se ha creado: {nombre_pdf}")
        else:
            print(f"No se encontró RUT en la página {i + 1}.")

separar_paginas_con_rut('sueldos.pdf')
