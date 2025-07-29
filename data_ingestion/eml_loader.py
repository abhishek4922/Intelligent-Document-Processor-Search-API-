import email
from bs4 import BeautifulSoup

def extract_text_from_eml(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        msg = email.message_from_file(f)

    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        elif part.get_content_type() == "text/html":
            html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, "html.parser")
            body += soup.get_text()
    return body
