import re
import spacy

# Load spaCy English model (make sure it's installed: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_invoice_metadata(text):
    metadata = {
        "invoice_number": None,
        "due_date": None,
        "total_amount": None
    }

    # --- Extract Invoice Number ---
    invoice_number_match = re.search(r"Invoice\s*Number[:\-]?\s*(\S+)", text, re.IGNORECASE)
    if invoice_number_match:
        metadata["invoice_number"] = invoice_number_match.group(1)

    # --- Extract Total Amount (Look for $ or ₹ or just digits) ---
    amount_match = re.search(r"(?:Total\s*Amount|Total)[:\-]?\s*\$?₹?\s*([0-9,]+(?:\.\d{1,2})?)", text, re.IGNORECASE)
    if amount_match:
        metadata["total_amount"] = amount_match.group(1)

    # --- Extract Due Date using spaCy NER ---
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "DATE" and "due" in ent.sent.text.lower():
            metadata["due_date"] = ent.text
            break

    return metadata
