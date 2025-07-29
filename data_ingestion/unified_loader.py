import os
from data_ingestion.pdf_loader import extract_text_from_pdf
from data_ingestion.docx_loader import extract_text_from_docx
from data_ingestion.txt_loader import extract_text_from_txt
from data_ingestion.eml_loader import extract_text_from_eml

def load_document(filepath):
    ext=os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        return extract_text_from_txt(filepath)
    elif ext == ".eml":
        return extract_text_from_eml(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    