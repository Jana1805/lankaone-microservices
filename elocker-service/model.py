import re
from typing import Optional
from pydantic import BaseModel, field_validator


VALID_DOCUMENT_TYPES = {"Birth Certificate", "Degree", "NIC", "Land Document"}
DATE_PATTERN = re.compile(r"^(0[1-9]|[12]\d|3[01])-(0[1-9]|1[0-2])-(\d{4})$")


class DocumentBase(BaseModel):
    citizen_id: str
    document_type: str
    file_url: str
    uploaded_at: str

    @field_validator("citizen_id")
    @classmethod
    def citizen_id_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("citizen_id must not be empty")
        return v.strip()

    @field_validator("document_type")
    @classmethod
    def validate_document_type(cls, v: str) -> str:
        if v not in VALID_DOCUMENT_TYPES:
            raise ValueError(
                f"document_type must be one of: {', '.join(sorted(VALID_DOCUMENT_TYPES))}"
            )
        return v

    @field_validator("file_url")
    @classmethod
    def file_url_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("file_url must not be empty")
        return v.strip()

    @field_validator("uploaded_at")
    @classmethod
    def validate_uploaded_at(cls, v: str) -> str:
        if not DATE_PATTERN.match(v):
            raise ValueError(
                "uploaded_at must be in DD-MM-YYYY format "
                "(day 01-31, month 01-12, year 4 digits)"
            )
        return v


class DocumentCreate(DocumentBase):
    """Schema for uploading a new document. ID is auto-generated."""
    pass


class DocumentUpdate(BaseModel):
    """Schema for updating document metadata. All fields optional."""
    citizen_id: Optional[str] = None
    document_type: Optional[str] = None
    file_url: Optional[str] = None
    uploaded_at: Optional[str] = None

    @field_validator("citizen_id")
    @classmethod
    def citizen_id_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("citizen_id must not be empty")
        return v.strip() if v else v

    @field_validator("document_type")
    @classmethod
    def validate_document_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in VALID_DOCUMENT_TYPES:
            raise ValueError(
                f"document_type must be one of: {', '.join(sorted(VALID_DOCUMENT_TYPES))}"
            )
        return v

    @field_validator("file_url")
    @classmethod
    def file_url_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("file_url must not be empty")
        return v.strip() if v else v

    @field_validator("uploaded_at")
    @classmethod
    def validate_uploaded_at(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not DATE_PATTERN.match(v):
            raise ValueError(
                "uploaded_at must be in DD-MM-YYYY format "
                "(day 01-31, month 01-12, year 4 digits)"
            )
        return v


class Document(DocumentBase):
    """Full document model returned from the service (includes generated ID)."""
    id: int

    class Config:
        from_attributes = True