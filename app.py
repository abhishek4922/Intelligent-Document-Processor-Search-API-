
# import streamlit as st
# import os
# import uuid
# from data_ingestion.unified_loader import load_document
# from classification.predict import classify_document
# from metadata_extract.resume_extractor import extract_resume_metadata
# from metadata_extract.invoice_extractor import extract_invoice_metadata
# from pymongo import MongoClient
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # MongoDB setup
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# client = MongoClient(MONGO_URI)
# db = client["doc_db"]
# collection = db["documents"]

# def main():
#     st.title("Document Processor")

#     uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt", "eml"])

#     if uploaded_file is not None:
#         if st.button("Process Document"):
#             # Save uploaded file temporarily
#             temp_dir = "temp_files"
#             if not os.path.exists(temp_dir):
#                 os.makedirs(temp_dir)
            
#             filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
#             filepath = os.path.join(temp_dir, filename)

#             with open(filepath, "wb") as f:
#                 f.write(uploaded_file.getbuffer())

#             with st.spinner("Processing..."):
#                 try:
#                     # Load document content
#                     content = load_document(filepath)

#                     # Classification
#                     doc_type = classify_document(content)
#                     # Classification
# # doc_type = classify_document(content)
#                     st.write("Predicted Document Type:", doc_type)  # <- Add this line


#                     # Extraction based on type
#                     if doc_type == "resume":
#                         metadata = extract_resume_metadata(content)
#                     elif doc_type == "invoice":
#                         metadata = extract_invoice_metadata(content)
#                     else:
#                         st.error(f"Unsupported document type: {doc_type}")
#                         return

#                     # Store in MongoDB
#                     record = {
#                         "filename": uploaded_file.name,
#                         "document_type": doc_type,
#                         "metadata": metadata
#                     }
#                     collection.insert_one(record)

#                     # Display results
#                     st.success("Document processed successfully!")
#                     st.write("Document Type:", doc_type)
#                     st.write("Metadata:", metadata)

#                 except Exception as e:
#                     st.error(f"An error occurred: {e}")
#                 finally:
#                     # Cleanup temp file
#                     if os.path.exists(filepath):
#                         os.remove(filepath)

# if __name__ == "__main__":
#     main()

import streamlit as st
import os
import uuid
import asyncio

from data_ingestion.unified_loader import load_document
from classification.predict import classify_document
from metadata_extract.resume_extractor import extract_resume_metadata
from metadata_extract.invoice_extractor import extract_invoice_metadata

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, JSON

# Set up database
DATABASE_URL = "sqlite+aiosqlite:///./docs.db"
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ✅ Corrected model
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    extracted_metadata = Column(JSON)  # ✅ Use a safe name here

# Initialize DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Insert into DB
async def insert_document(filename, doc_type, metadata):
    async with async_session() as session:
        doc = Document(
            filename=filename,
            document_type=doc_type,
            extracted_metadata=metadata  # ✅ Match the column name
        )
        session.add(doc)
        await session.commit()

# Streamlit main function
def main():
    st.title("📄 Document Classifier & Metadata Extractor")

    uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "txt", "eml"])

    if uploaded_file is not None:
        if st.button("Process Document"):
            temp_dir = "temp_files"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
            filepath = os.path.join(temp_dir, filename)

            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Processing..."):
                try:
                    # Load & classify
                    content = load_document(filepath)
                    doc_type = classify_document(content)
                    st.write("Predicted Document Type:", doc_type)

                    # Extract metadata
                    if doc_type == "resume":
                        metadata = extract_resume_metadata(content)
                    elif doc_type == "invoice":
                        metadata = extract_invoice_metadata(content)
                    else:
                        st.error(f"Unsupported document type: {doc_type}")
                        return

                    # Insert to SQL DB
                    asyncio.run(insert_document(uploaded_file.name, doc_type, metadata))

                    st.success("✅ Document processed and saved!")
                    st.write("**Document Type:**", doc_type)
                    st.json(metadata)

                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)

# Run app and DB initialization
if __name__ == "__main__":
    asyncio.run(init_db())
    main()
