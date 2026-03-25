from typing import List, Optional
from model import Beneficiary, BeneficiaryCreate, BeneficiaryUpdate, IncomeLevelEnum, StatusEnum
from data_service import data_service


class BeneficiaryService:
    def __init__(self):
        self.data_service = data_service
    
    def _determine_eligibility(self, income_level: IncomeLevelEnum) -> tuple[StatusEnum, float]:
        if income_level == IncomeLevelEnum.LOW:
            return StatusEnum.ELIGIBLE, 7500.0
        elif income_level == IncomeLevelEnum.MEDIUM:
            return StatusEnum.UNDER_REVIEW, 3500.0
        else:  # HIGH
            return StatusEnum.INELIGIBLE, 0.0
    
    def apply_for_beneficiary(self, beneficiary_data: BeneficiaryCreate) -> Beneficiary:
        status, monthly_allowance = self._determine_eligibility(beneficiary_data.income_level)
        
        full_beneficiary = Beneficiary(
            id=0,  # Will be set by data service
            citizen_id=beneficiary_data.citizen_id,
            program=beneficiary_data.program,
            income_level=beneficiary_data.income_level,
            status=status,
            monthly_allowance=monthly_allowance
        )
        
        return self.data_service.create_beneficiary(full_beneficiary)
    
    def get_all_beneficiaries(self) -> List[Beneficiary]:
        return self.data_service.get_all_beneficiaries()
    
    def get_beneficiary_by_citizen_id(self, citizen_id: str) -> Optional[Beneficiary]:
        return self.data_service.get_beneficiary_by_citizen_id(citizen_id)
    
    def update_beneficiary(self, citizen_id: str, update_data: BeneficiaryUpdate) -> Optional[Beneficiary]:
        existing_beneficiary = self.data_service.get_beneficiary_by_citizen_id(citizen_id)
        if not existing_beneficiary:
            return None
        
        if update_data.income_level is not None:
            status, monthly_allowance = self._determine_eligibility(update_data.income_level)
            existing_beneficiary.status = status
            existing_beneficiary.monthly_allowance = monthly_allowance
        
        updated_beneficiary = self.data_service.update_beneficiary_by_citizen_id(citizen_id, update_data)
        return updated_beneficiary
    
    def delete_beneficiary(self, beneficiary_id: int) -> bool:
        return self.data_service.delete_beneficiary_by_id(beneficiary_id)


beneficiary_service = BeneficiaryService()