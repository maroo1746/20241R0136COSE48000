from PyPDF2 import PdfReader
from fastapi import UploadFile


def ocr(file: UploadFile):
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
