from typing import List, Optional, Dict
from model import Beneficiary, BeneficiaryCreate, BeneficiaryUpdate, ProgramEnum, IncomeLevelEnum, StatusEnum


class InMemoryDataService:
    def __init__(self):
        self.beneficiaries: Dict[int, Beneficiary] = {}
        self.next_id = 1
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        mock_beneficiaries = [
            Beneficiary(
                id=self.next_id,
                citizen_id="CIT001",
                program=ProgramEnum.ASWESUMA,
                income_level=IncomeLevelEnum.LOW,
                status=StatusEnum.ELIGIBLE,
                monthly_allowance=7500.0
            ),
            Beneficiary(
                id=self.next_id + 1,
                citizen_id="CIT002",
                program=ProgramEnum.SAMURDHI,
                income_level=IncomeLevelEnum.MEDIUM,
                status=StatusEnum.UNDER_REVIEW,
                monthly_allowance=3500.0
            ),
            Beneficiary(
                id=self.next_id + 2,
                citizen_id="CIT003",
                program=ProgramEnum.ELDERLY_SUPPORT,
                income_level=IncomeLevelEnum.HIGH,
                status=StatusEnum.INELIGIBLE,
                monthly_allowance=0.0
            )
        ]
        
        for beneficiary in mock_beneficiaries:
            self.beneficiaries[beneficiary.id] = beneficiary
        
        self.next_id += 3
    
    def create_beneficiary(self, beneficiary: Beneficiary) -> Beneficiary:
        beneficiary_id = self.next_id
        self.next_id += 1
        
        beneficiary.id = beneficiary_id
        self.beneficiaries[beneficiary_id] = beneficiary
        return beneficiary
    
    def get_all_beneficiaries(self) -> List[Beneficiary]:
        return list(self.beneficiaries.values())
    
    def get_beneficiary_by_citizen_id(self, citizen_id: str) -> Optional[Beneficiary]:
        for beneficiary in self.beneficiaries.values():
            if beneficiary.citizen_id == citizen_id:
                return beneficiary
        return None
    
    def get_beneficiary_by_id(self, beneficiary_id: int) -> Optional[Beneficiary]:
        return self.beneficiaries.get(beneficiary_id)
    
    def update_beneficiary_by_citizen_id(self, citizen_id: str, update_data: BeneficiaryUpdate) -> Optional[Beneficiary]:
        beneficiary = self.get_beneficiary_by_citizen_id(citizen_id)
        if not beneficiary:
            return None
        
        if update_data.program is not None:
            beneficiary.program = update_data.program
        if update_data.income_level is not None:
            beneficiary.income_level = update_data.income_level
        
        return beneficiary
    
    def delete_beneficiary_by_id(self, beneficiary_id: int) -> bool:
        if beneficiary_id in self.beneficiaries:
            del self.beneficiaries[beneficiary_id]
            return True
        return False


data_service = InMemoryDataService()