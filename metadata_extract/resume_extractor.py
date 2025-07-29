import re
import spacy

# Load spaCy English model (make sure it's installed: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def extract_resume_metadata(text):
    metadata = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": []
    }

    # --- Extract Name using spaCy NER (looking for PERSON entities) ---
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            metadata["name"] = ent.text
            break

    # --- Extract Email ---
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        metadata["email"] = email_match.group(0)

    # --- Extract Phone Number (simple format) ---
    phone_match = re.search(r"\+?\d{1,3}[-\s]?\(?\d{1,4}\)?[-\s]?\d{1,4}[-\s]?\d{1,4}", text)
    if phone_match:
        metadata["phone"] = phone_match.group(0)

    # --- Extract Skills (example: Python, SQL, Machine Learning) ---
    skill_keywords = ["python", "sql", "java", "javascript", "machine learning", "deep learning", "data science", "aws", "docker", "html", "css"]
    skills_found = [skill for skill in skill_keywords if skill.lower() in text.lower()]
    metadata["skills"] = skills_found

    return metadata
