from cx_Freeze import setup, Executable
import sys
import os


if getattr(sys, 'frozen', False):  
    tesseract_path = os.path.join(sys._MEIPASS, 'tesseract-ocr')
else:  
    tesseract_path = os.path.join(os.path.dirname(__file__), 'tesseract-ocr')

include_files = [
    (os.path.join(tesseract_path, 'tesseract.exe'), 'tesseract-ocr/tesseract.exe'),
    (os.path.join(tesseract_path, 'tessdata'), 'tesseract-ocr/tessdata')
]


executables = [
    Executable(
        script="separar_pdf.py", 
        base="Win32GUI",  
        icon=None 
    )
]


setup(
    name="SepararPDF", 
    version="1.0",
    description="Aplicación para separar PDFs",  
    options={  
        'build_exe': {
            'packages': ['os', 'sys', 'fitz', 'PIL', 'pytesseract', 're'],  
            'include_files': include_files,  
            'excludes': [],  
        }
    },
    executables=executables  
)
