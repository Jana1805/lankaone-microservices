# identity-service/model.py
from pydantic import BaseModel, field_validator
from typing import Optional
import re


class Identity(BaseModel):
    id: int
    nic: str
    name: str
    dob: str  # Format: DD-MM-YYYY
    biometric_hash: str
    status: str  # "Verified", "Pending", "Rejected"


class IdentityCreate(BaseModel):
    nic: str
    name: str
    dob: str  # Format: DD-MM-YYYY
    biometric_hash: str

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value):
        pattern = r"^\d{2}-\d{2}-\d{4}$"
        if not re.match(pattern, value):
            raise ValueError("Date must be in DD-MM-YYYY format (e.g. 12-05-2000)")
        day, month, year = value.split("-")
        if not (1 <= int(day) <= 31):
            raise ValueError("Day must be between 01 and 31")
        if not (1 <= int(month) <= 12):
            raise ValueError("Month must be between 01 and 12")
        if not (1900 <= int(year) <= 2025):
            raise ValueError("Year must be between 1900 and 2025")
        return value

    @field_validator("nic")
    @classmethod
    def validate_nic(cls, value):
        # Sri Lankan NIC: 9 digits + V/X  or 12 digits
        pattern = r"^\d{9}[VXvx]$|^\d{12}$"
        if not re.match(pattern, value):
            raise ValueError("NIC must be 9 digits followed by V or X, or 12 digits (e.g. 200012345678)")
        return value


class IdentityUpdate(BaseModel):
    name: Optional[str] = None
    dob: Optional[str] = None
    biometric_hash: Optional[str] = None
    status: Optional[str] = None

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, value):
        if value is None:
            return value
        pattern = r"^\d{2}-\d{2}-\d{4}$"
        if not re.match(pattern, value):
            raise ValueError("Date must be in DD-MM-YYYY format (e.g. 12-05-2000)")
        day, month, year = value.split("-")
        if not (1 <= int(day) <= 31):
            raise ValueError("Day must be between 01 and 31")
        if not (1 <= int(month) <= 12):
            raise ValueError("Month must be between 01 and 12")
        if not (1900 <= int(year) <= 2025):
            raise ValueError("Year must be between 1900 and 2025")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            return value
        allowed = ["Verified", "Pending", "Rejected"]
        if value not in allowed:
            raise ValueError(f"Status must be one of: {allowed}")
        return value