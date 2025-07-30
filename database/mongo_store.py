from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Set this to your Mongo URI
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "document_db"
COLLECTION_NAME = "documents"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def store_document_result(filepath, doc_type, metadata):
    doc_record = {
        "file_path": filepath,
        "type": doc_type,
        "metadata": metadata
    }
    result = collection.insert_one(doc_record)
    return result.inserted_id
