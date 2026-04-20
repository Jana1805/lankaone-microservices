from typing import List, Optional
from model import Document, DocumentCreate, DocumentUpdate


class DocumentMockDataService:
    """In-memory mock data store for documents with full CRUD operations."""     

    def __init__(self):
        self._documents: List[Document] = [
            Document(
                id=1,
                citizen_id="SLUDI10001",
                document_type="Birth Certificate",
                file_url="storage/bc_001.pdf",
                uploaded_at="10-03-2024",
            ),
            Document(
                id=2,
                citizen_id="SLUDI10001",
                document_type="Degree",
                file_url="storage/deg_001.pdf",
                uploaded_at="15-06-2024",
            ),
            Document(
                id=3,
                citizen_id="SLUDI10002",
                document_type="NIC",
                file_url="storage/nic_002.pdf",
                uploaded_at="20-01-2024",
            ),
        ]
        self._next_id: int = 4

    # ------------------------------------------------------------------ #
    # Read operations                                                    #
    # ------------------------------------------------------------------ #

    def get_all(self) -> List[Document]:
        """Return all documents."""
        return self._documents

    def get_by_citizen_id(self, citizen_id: str) -> List[Document]:
        """Return all documents belonging to a specific citizen."""
        return [d for d in self._documents if d.citizen_id == citizen_id]

    def get_by_citizen_and_doc_id(
        self, citizen_id: str, doc_id: int
    ) -> Optional[Document]:
        """Return a specific document by citizen ID and document ID."""
        for doc in self._documents:
            if doc.citizen_id == citizen_id and doc.id == doc_id:
                return doc
        return None

    def get_by_id(self, doc_id: int) -> Optional[Document]:
        """Return a document by its auto-generated ID."""
        for doc in self._documents:
            if doc.id == doc_id:
                return doc
        return None

    # ------------------------------------------------------------------ #
    # Write operations                                                      #
    # ------------------------------------------------------------------ #

    def create(self, data: DocumentCreate) -> Document:
        """Insert a new document and return it with its generated ID."""
        new_doc = Document(id=self._next_id, **data.model_dump())
        self._next_id += 1
        self._documents.append(new_doc)
        return new_doc

    def update(self, doc_id: int, data: DocumentUpdate) -> Optional[Document]:
        """Apply partial updates to an existing document. Returns None if not found."""
        for index, doc in enumerate(self._documents):
            if doc.id == doc_id:
                updated_data = doc.model_dump()
                patch = data.model_dump(exclude_unset=True)
                updated_data.update(patch)
                updated_doc = Document(**updated_data)
                self._documents[index] = updated_doc
                return updated_doc
        return None

    def delete(self, doc_id: int) -> bool:
        """Delete a document by ID. Returns True if deleted, False if not found."""
        for index, doc in enumerate(self._documents):
            if doc.id == doc_id:
                self._documents.pop(index)
                return True
        return False   