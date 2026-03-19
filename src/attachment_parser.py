# src/attachment_parser.py
import os
from PyPDF2 import PdfReader
from docx import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTACHMENTS_DIR = os.path.join(BASE_DIR, "data", "attachments")

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def parse_attachment(filename):
    file_path = os.path.join(ATTACHMENTS_DIR, filename)

    if filename.endswith(".txt"):
        return read_txt(file_path)
    elif filename.endswith(".pdf"):
        return read_pdf(file_path)
    elif filename.endswith(".docx"):
        return read_docx(file_path)
    else:
        return ""