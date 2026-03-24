# identity-service/main.py
from fastapi import FastAPI, HTTPException, status
from model import Identity, IdentityCreate, IdentityUpdate
from service import IdentityService
from typing import List

app = FastAPI(title="LankaOne – Identity Microservice", version="1.0.0")

# Initialize service
identity_service = IdentityService()


@app.get("/")
def read_root():
    return {"message": "LankaOne Identity Microservice is running"}


@app.get("/api/identities", response_model=List[Identity])
def get_all_identities():
    """Get all registered identities"""
    return identity_service.get_all()


@app.get("/api/identities/{identity_id}", response_model=Identity)
def get_identity(identity_id: int):
    """Get an identity by ID"""
    identity = identity_service.get_by_id(identity_id)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found")
    return identity


@app.get("/api/identities/nic/{nic}", response_model=Identity)
def get_identity_by_nic(nic: str):
    """Get an identity by NIC"""
    identity = identity_service.get_by_nic(nic)
    if not identity:
        raise HTTPException(status_code=404, detail="Identity not found for given NIC")
    return identity


@app.post("/api/identities", response_model=Identity, status_code=status.HTTP_201_CREATED)
def create_identity(identity: IdentityCreate):
    """Register a new citizen identity"""
    existing = identity_service.get_by_nic(identity.nic)
    if existing:
        raise HTTPException(status_code=409, detail="NIC already registered")
    return identity_service.create(identity)


@app.put("/api/identities/nic/{nic}", response_model=Identity)
def update_identity_by_nic(nic: str, identity: IdentityUpdate):
    """Update an identity by NIC"""
    updated = identity_service.update_by_nic(nic, identity)
    if not updated:
        raise HTTPException(status_code=404, detail="Identity not found for given NIC")
    return updated


@app.delete("/api/identities/nic/{nic}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identity_by_nic(nic: str):
    """Delete an identity by NIC"""
    success = identity_service.delete_by_nic(nic)
    if not success:
        raise HTTPException(status_code=404, detail="Identity not found for given NIC")
    return None