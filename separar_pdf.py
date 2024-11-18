# una app que a los pdf lo sepáre por paginas, cada pdf que separe llevara el nombre del rut, tendra dos opciones para el nombre,segun el tipo de archivo, si es un certificado, el nombre del pdf sera el rut del cliente sin digito verificador, sino que dira cer, ejemplo, xx.xxx.xxx-cer, si es un sueldo el nombre del pdf sera xx.xxx.xxx, el pdf que hay que separar contiene en cada pagina datos de un cliente y en vez de que sea todos los clientes en un pdf hay que hacer un pdf por cliente, asi cada hoja el pdf se tiene que hacer un pdf pip install PyPDF2
import PyPDF2

def separar_paginas(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_paginas = len(pdf_reader.pages)
        
        for i in range(num_paginas):
            pdf_writer = PyPDF2.PdfWriter()
            pagina = pdf_reader.pages[i]
            pdf_writer.add_page(pagina)
            
            with open(f"pagina_{i+1}.pdf", 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            print(f"Se ha creado: pagina_{i+1}.pdf")

separar_paginas('sueldos.pdf')
