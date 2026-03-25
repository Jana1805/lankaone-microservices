from fastapi import FastAPI, HTTPException, Path
from typing import List
from model import Beneficiary, BeneficiaryCreate, BeneficiaryUpdate
from service import beneficiary_service

app = FastAPI(title="Beneficiary Service", description="Microservice for beneficiary management")


@app.get("/api/beneficiary/list", response_model=List[Beneficiary])
async def get_all_beneficiaries():
    """Get all beneficiaries"""
    return beneficiary_service.get_all_beneficiaries()


@app.get("/api/beneficiary/{citizen_id}", response_model=Beneficiary)
async def get_beneficiary_by_citizen_id(citizen_id: str = Path(..., description="Citizen ID")):
    """Get beneficiary by citizen ID"""
    beneficiary = beneficiary_service.get_beneficiary_by_citizen_id(citizen_id)
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary


@app.post("/api/beneficiary/apply", response_model=Beneficiary)
async def apply_for_beneficiary(beneficiary_data: BeneficiaryCreate):
    """Apply for beneficiary program"""
    existing_beneficiary = beneficiary_service.get_beneficiary_by_citizen_id(beneficiary_data.citizen_id)
    if existing_beneficiary:
        raise HTTPException(status_code=400, detail="Beneficiary with this citizen ID already exists")
    
    return beneficiary_service.apply_for_beneficiary(beneficiary_data)


@app.put("/api/beneficiary/{citizen_id}", response_model=Beneficiary)
async def update_beneficiary(
    citizen_id: str = Path(..., description="Citizen ID"),
    update_data: BeneficiaryUpdate = None
):
    """Update beneficiary by citizen ID"""
    beneficiary = beneficiary_service.update_beneficiary(citizen_id, update_data)
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary


@app.delete("/api/beneficiary/{id}")
async def delete_beneficiary(id: int = Path(..., description="Beneficiary ID")):
    """Delete beneficiary by ID"""
    success = beneficiary_service.delete_beneficiary(id)
    if not success:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return {"message": "Beneficiary deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8084)