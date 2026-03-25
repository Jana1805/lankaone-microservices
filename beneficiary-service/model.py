from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProgramEnum(str, Enum):
    ASWESUMA = "Aswesuma"
    SAMURDHI = "Samurdhi"
    ELDERLY_SUPPORT = "Elderly Support"


class IncomeLevelEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class StatusEnum(str, Enum):
    ELIGIBLE = "Eligible"
    INELIGIBLE = "Ineligible"
    UNDER_REVIEW = "Under Review"


class BeneficiaryBase(BaseModel):
    citizen_id: str = Field(..., min_length=1, description="Citizen ID")
    program: ProgramEnum
    income_level: IncomeLevelEnum


class BeneficiaryCreate(BaseModel):
    citizen_id: str = Field(..., min_length=1, description="Citizen ID")
    program: ProgramEnum
    income_level: IncomeLevelEnum


class BeneficiaryUpdate(BaseModel):
    program: Optional[ProgramEnum] = None
    income_level: Optional[IncomeLevelEnum] = None


class Beneficiary(BaseModel):
    id: int
    citizen_id: str
    program: ProgramEnum
    income_level: IncomeLevelEnum
    status: StatusEnum
    monthly_allowance: float = Field(..., ge=0)

    class Config:
        from_attributes = True