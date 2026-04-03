import re
from pydantic import BaseModel, field_validator
from typing import Optional


VALID_PAYMENT_TYPES = ["Electricity Bill", "Water Bill", "Tax", "Government Fee"]
VALID_METHODS = ["Card", "Bank Transfer", "Mobile Pay"]
VALID_STATUSES = ["SUCCESS", "PENDING", "FAILED", "REFUNDED"]


class PaymentCreate(BaseModel):
    citizen_id: str
    payment_type: str
    amount: float
    method: str

#citizen_id Validation

    @field_validator("citizen_id")
    @classmethod
    def citizen_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("citizen_id must not be empty")
        return v.strip()

#Only predefined payment types are allowed (Water Bill, Electricity Bill, Tax, Government Fee)

    @field_validator("payment_type")
    @classmethod
    def validate_payment_type(cls, v):
        if v not in VALID_PAYMENT_TYPES:
            raise ValueError(f"payment_type must be one of: {', '.join(VALID_PAYMENT_TYPES)}")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        return v

#Success,pending,failed,refunded

    @field_validator("method")
    @classmethod
    def validate_method(cls, v):
        if v not in VALID_METHODS:
            raise ValueError(f"method must be one of: {', '.join(VALID_METHODS)}")
        return v


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(VALID_STATUSES)}")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError("amount must be greater than 0")
        return v


class Payment(BaseModel):
    id: int
    payment_id: str
    citizen_id: str
    payment_type: str
    amount: float
    method: str
    status: str