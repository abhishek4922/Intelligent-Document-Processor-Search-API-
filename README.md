# Document Processor

This project is a comprehensive document processing application designed to automatically classify and extract metadata from various document types, including resumes, invoices, and more. It provides two primary interfaces: an interactive web application built with Streamlit and a robust REST API powered by FastAPI.

## Features

- **Multi-Format Document Support:** Ingests and processes various file formats, including `.pdf`, `.docx`, `.txt`, and `.eml`.
- **Automatic Document Classification:** Utilizes a pre-trained machine learning model to classify documents into categories like "resume" or "invoice".
- **Metadata Extraction:** Extracts relevant information based on the document type. For example:
    - **Resumes:** Extracts contact information, skills, experience, etc.
    - **Invoices:** Extracts invoice number, dates, total amount, etc.
- **Dual Interfaces:**
    - **Streamlit Web App:** An easy-to-use interface for uploading documents and viewing the extracted results in real-time.
    - **FastAPI Backend:** A scalable API for programmatic access and integration with other systems.
- **Asynchronous Database:** Uses SQLAlchemy with `aiosqlite` for asynchronous database operations, storing all processing results in a local SQLite database.

## Architecture

The application is structured into several key components:

- **Data Ingestion (`data_ingestion/`):** A unified loader that handles various document types, using specialized modules for each format.
- **Classification (`classification/`):** A machine learning pipeline that predicts the document type using a model trained with Scikit-learn and spaCy.
- **Metadata Extraction (`metadata_extract/`):** Specialized extractors for each document category that pull out structured data.
- **Database (`router/database.py`, `router/models.py`):** An asynchronous database layer using SQLAlchemy to interact with a SQLite database (`docs.db`).
- **API (`router/router.py`):** The FastAPI router that defines all API endpoints for document upload and retrieval.
- **Web Application (`app.py`):** The Streamlit application that provides a user-friendly front-end.

## Technologies Used

- **Backend:** FastAPI, Uvicorn
- **Web Frontend:** Streamlit
- **Machine Learning:** Scikit-learn, spaCy, Pandas
- **Database:** SQLAlchemy, aiosqlite
- **File Processing:** `pdfplumber`, `python-docx`, `beautifulsoup4`

## Setup and Installation

Follow these steps to set up and run the project locally.

**1. Clone the Repository**
```bash
git clone <repository-url>
cd doc_processor
```

**2. Create and Activate a Virtual Environment**
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
Install all required packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**4. Download spaCy Model**
The project uses a spaCy model for Natural Language Processing. Download the required model.
```bash
python -m spacy download en_core_web_sm
```

**5. Initialize the Database**
The database will be initialized automatically when you run either the Streamlit app or the FastAPI server for the first time.

## Usage

You can interact with this project through either the Streamlit web app or the FastAPI server.

### Option 1: Running the Streamlit Web App

This is the simplest way to test the application's functionality.

```bash
streamlit run app.py
```

Navigate to the URL provided by Streamlit (usually `http://localhost:8501`). You can upload a document and see the classification and extracted metadata directly in your browser.

### Option 2: Running the FastAPI Server

This provides a REST API for integration with other services.

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

#### API Endpoints

- **`POST /api/upload/`**
  - Upload a document for processing.
  - **Request:** `multipart/form-data` with a `file` field containing the document.
  - **Response:** A JSON object with the `document_type` and extracted `metadata`.

- **`GET /api/documents/`**
  - Retrieve a list of all processed documents from the database.

- **`GET /api/info`**
  - Get basic information about the running service.

## Project Structure

```
.
├── app.py                  # Streamlit web application
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── docs.db                 # SQLite database file
├── .env                    # Environment variables (if any)
├── classification/         # Document classification module
│   ├── predict.py
│   └── train_model.py
├── data_ingestion/         # Document loading and parsing module
│   └── unified_loader.py
├── metadata_extract/       # Metadata extraction module
│   ├── invoice_extractor.py
│   └── resume_extractor.py
├── models/                 # Trained ML models
│   └── doc_classifier.pkl
├── router/                 # FastAPI routing and DB logic
│   ├── router.py
│   ├── database.py
│   └── models.py
└── temp_files/             # Temporary storage for uploaded files
```
