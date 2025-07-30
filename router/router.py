# # from classification.predict import classify_document
# # from data_ingestion.unified_loader import load_document
# # from metadata_extract.resume_extractor import extract_resume_metadata
# # from metadata_extract.invoice_extractor import extract_invoice_metadata

# # from db.mongo_store import store_document_result

# # def route_document(filepath):
# #     text = load_document(filepath)
# #     doc_type = classify_document(text)

# #     if doc_type == "resume":
# #         metadata = extract_resume_metadata(text)
# #     elif doc_type == "invoice":
# #         metadata = extract_invoice_metadata(text)
# #     else:
# #         metadata = {"error": f"Unsupported document type: {doc_type}"}

# #     # Store in MongoDB
# #     store_document_result(filepath, doc_type, metadata)

# #     return {
# #         "type": doc_type,
# #         "metadata": metadata
# #     }

# from fastapi import APIRouter, UploadFile, File
# from fastapi.responses import JSONResponse
# import os
# import uuid

# from data_ingestion.unified_loader import load_document
# from classification.predict import classify_document
# from metadata_extract.resume_extractor import extract_resume_metadata
# from metadata_extract.invoice_extractor import extract_invoice_metadata
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# from pymongo import MongoClient

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
# client = MongoClient(MONGO_URI)
# db = client["doc_db"]
# collection = db["documents"]

# router = APIRouter()

# @router.post("/upload/")
# async def upload_document(file: UploadFile = File(...)):
#     try:
#         # Save file temporarily
#         filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
#         filepath = os.path.join("data", filename)

#         with open(filepath, "wb") as f:
#             f.write(await file.read())

#         # Load document content
#         content = load_document(filepath)

#         # Classification
#         doc_type = classify_document(content)

#         # Extraction based on type
#         if doc_type == "resume":
#             metadata = extract_resume_metadata(content)
#         elif doc_type == "invoice":
#             metadata = extract_invoice_metadata(content)
#         else:
#             return JSONResponse(
#                 status_code=400,
#                 content={"error": f"Unsupported document type: {doc_type}"}
#             )

#         # Store in MongoDB
#         record = {
#             "filename": file.filename,
#             "document_type": doc_type,
#             "metadata": metadata
#         }
#         collection.insert_one(record)

#         # Cleanup temp file
#         os.remove(filepath)

#         return {"document_type": doc_type, "metadata": metadata}

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})

# @router.get("/info")
# async def get_info():
#     return {
#         "version": "1.0.0",
#         "status": "running",
#         "developer": "Abhishek Jain SDE"
#     }


from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import os, uuid
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from models import Document
from sqlalchemy.future import select

from data_ingestion.unified_loader import load_document
from classification.predict import classify_document
from metadata_extract.resume_extractor import extract_resume_metadata
from metadata_extract.invoice_extractor import extract_invoice_metadata

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        # Save file temporarily
        filename = f"temp_{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join("data", filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())

        # Load document content
        content = load_document(filepath)

        # Classification
        doc_type = classify_document(content)

        # Extraction based on type
        if doc_type == "resume":
            metadata = extract_resume_metadata(content)
        elif doc_type == "invoice":
            metadata = extract_invoice_metadata(content)
        else:
            return JSONResponse(status_code=400, content={"error": f"Unsupported document type: {doc_type}"})

        # Save to DB
        doc = Document(
            filename=file.filename,
            document_type=doc_type,
            metadata=metadata
        )
        db.add(doc)
        await db.commit()

        # Cleanup
        os.remove(filepath)

        return {"document_type": doc_type, "metadata": metadata}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

