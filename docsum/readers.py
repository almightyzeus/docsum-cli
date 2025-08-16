import os
from docx import Document
from PyPDF2 import PdfReader
from PyPDF2.errors import FileNotDecryptedError

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except FileNotDecryptedError:
        raise ValueError("PDF is password protected (file not decrypted)")

def extract_text_from_txt(txt_path: str) -> str:
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        raise ValueError("TXT file may be encrypted or not a valid text file")
    except PermissionError:
        raise ValueError("TXT file is locked or you do not have permission to read it")
    except OSError as e:
        raise ValueError(f"TXT file is corrupted or unreadable: {e}")

def extract_text_from_docx(docx_path: str) -> str:
    import zipfile
    try:
        doc = Document(docx_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except PermissionError:
        raise ValueError("DOCX file is locked or you do not have permission to read it")
    except zipfile.BadZipFile:
        raise ValueError("DOCX file is corrupted or unreadable")
    except Exception as e:
        if "password" in str(e).lower():
            raise ValueError("DOCX is password protected or unreadable")
        raise ValueError(f"DOCX file error: {e}")
