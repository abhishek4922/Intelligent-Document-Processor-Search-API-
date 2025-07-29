from docx import Document

def extract_text_from_docx(filepath):
    doc=Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

