from fastapi import FastAPI, HTTPException, status
from typing import List

from model import Document, DocumentCreate, DocumentUpdate
from service import DocumentService

app = FastAPI(
    title="LankaOne – E-Locker Service",
    description=(
        "Secure digital document storage for Sri Lankan citizens. "
        "Supports Birth Certificates, Degrees, NICs, and Land Documents."
    ),
    version="1.0.0",
)

_service = DocumentService()


# ------------------------------------------------------------------ #
# GET /api/documents – list all documents                             #
# ------------------------------------------------------------------ #
@app.get(
    "/api/documents",
    response_model=List[Document],
    status_code=status.HTTP_200_OK,
    summary="Get all documents",
)
def get_all_documents():
    """Return every document stored in the E-Locker."""
    return _service.get_all_documents()


# ------------------------------------------------------------------ #
# GET /api/documents/{citizen_id} – all docs for a citizen            #
# ------------------------------------------------------------------ #
@app.get(
    "/api/documents/{citizen_id}",
    response_model=List[Document],
    status_code=status.HTTP_200_OK,
    summary="Get all documents for a citizen",
)
def get_documents_by_citizen(citizen_id: str):
    """
    Return all documents associated with a given citizen ID.
    Returns an empty list (200) if the citizen exists but has no documents.
    """
    documents = _service.get_documents_by_citizen(citizen_id)
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No documents found for citizen_id '{citizen_id}'.",
        )
    return documents


# ------------------------------------------------------------------ #
# GET /api/documents/{citizen_id}/{doc_id} – specific document        #
# ------------------------------------------------------------------ #
@app.get(
    "/api/documents/{citizen_id}/{doc_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    summary="Get a specific document for a citizen",
)
def get_document(citizen_id: str, doc_id: int):
    """Return a single document identified by citizen ID and document ID."""
    doc = _service.get_document_by_citizen_and_id(citizen_id, doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id={doc_id} not found for citizen_id '{citizen_id}'.",
        )
    return doc


# ------------------------------------------------------------------ #
# POST /api/documents/upload – upload a new document                  #
# ------------------------------------------------------------------ #
@app.post(
    "/api/documents/upload",
    response_model=Document,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new document",
)
def upload_document(data: DocumentCreate):
    """
    Upload a new official document to the citizen's E-Locker.

    **Validation rules:**
    - `document_type` must be one of: Birth Certificate, Degree, NIC, Land Document
    - `citizen_id` and `file_url` must not be empty
    - `uploaded_at` must follow DD-MM-YYYY format
    """
    return _service.upload_document(data)


# ------------------------------------------------------------------ #
# PUT /api/documents/{doc_id} – update document metadata              #
# ------------------------------------------------------------------ #
@app.put(
    "/api/documents/{doc_id}",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    summary="Update document metadata",
)
def update_document(doc_id: int, data: DocumentUpdate):
    """
    Partially update an existing document's metadata.
    Only the fields provided in the request body will be changed.
    """
    doc = _service.update_document(doc_id, data)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id={doc_id} not found.",
        )
    return doc


# ------------------------------------------------------------------ #
# DELETE /api/documents/{doc_id} – delete a document                  #
# ------------------------------------------------------------------ #
@app.delete(
    "/api/documents/{doc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document",
)
def delete_document(doc_id: int):
    """Permanently delete a document from the E-Locker by its ID."""
    deleted = _service.delete_document(doc_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id={doc_id} not found.",
        )