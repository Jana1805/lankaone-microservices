from typing import List, Optional
from model import Document, DocumentCreate, DocumentUpdate
from data_service import DocumentMockDataService


class DocumentService:
    """Business logic layer – delegates all data operations to DocumentMockDataService."""

    def __init__(self):
        self._data_service = DocumentMockDataService()

    def get_all_documents(self) -> List[Document]:
        """Retrieve every document in the store."""
        return self._data_service.get_all()

    def get_documents_by_citizen(self, citizen_id: str) -> List[Document]:
        """Retrieve all documents belonging to a citizen."""
        return self._data_service.get_by_citizen_id(citizen_id)

    def get_document_by_citizen_and_id(
        self, citizen_id: str, doc_id: int
    ) -> Optional[Document]:
        """Retrieve a single document by citizen ID + document ID combination."""
        return self._data_service.get_by_citizen_and_doc_id(citizen_id, doc_id)

    def upload_document(self, data: DocumentCreate) -> Document:
        """Upload (create) a new document entry."""
        return self._data_service.create(data)

    def update_document(self, doc_id: int, data: DocumentUpdate) -> Optional[Document]:
        """Update document metadata. Returns None if document does not exist."""
        return self._data_service.update(doc_id, data)

    def delete_document(self, doc_id: int) -> bool:
        """Delete a document by ID. Returns True if successful, False if not found."""
        return self._data_service.delete(doc_id)