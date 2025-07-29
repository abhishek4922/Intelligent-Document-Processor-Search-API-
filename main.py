from metadata_extract.resume_extractor import extract_resume_metadata
from data_ingestion.unified_loader import load_document

filepath="C:/Users/abhis/Desktop/Projects/web/proj/docextract/doc_processor/ABHISHEK_JAIN_RESUME (12).pdf"
text = load_document(filepath)
metadata = extract_resume_metadata(text)
# doc_processor\metadata_extraction.py\resume_extractor.py
print("Extracted Metadata:")
for key, value in metadata.items():
    print(f"{key}: {value}")

    # filepath="C:/Users/abhis/Desktop/Projects/web/proj/docextract/doc_processor/ABHISHEK_JAIN_RESUME (12).pdf"
    # text=load_document(filepath)
    # print("Extracted Text:\n", text[:1000])  # Print first 1000 characters
