# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import JSONResponse
import httpx
from typing import Any
from auth import verify_token, create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#member 4
from pydantic import BaseModel
from typing import Optional
from enum import Enum

# Security dependency for Swagger
security = HTTPBearer()

app = FastAPI(title="LankaOne – API Gateway", version="1.0.0")

# -------------------------
# Services
# -------------------------
SERVICES = {
    "identity":    "http://localhost:8081",
    "elocker":     "http://localhost:8082",
    "govpay":      "http://localhost:8083",
    "beneficiary": "http://localhost:8084",
}

# -------------------------
# Middleware: Logging
# -------------------------
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

# -------------------------
# Forwarding function
# -------------------------
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            try:
                data = response.json() if response.content else None
            except ValueError:
                data = None

            return JSONResponse(content=data, status_code=response.status_code)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

# -------------------------
# Token endpoint
# -------------------------
@app.post("/token")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "password":
        token = create_access_token({"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# -------------------------
# Root
# -------------------------
@app.get("/")
def read_root():
    return {
        "message": "LankaOne API Gateway is running",
        "available_services": list(SERVICES.keys())
    }

# -------------------------
# Identity Routes (Member 1)
# -------------------------
@app.get("/gateway/identities", dependencies=[Depends(security)])
async def get_all_identities():
    return await forward_request("identity", "/api/identities", "GET")

@app.get("/gateway/identities/{identity_id}", dependencies=[Depends(security)])
async def get_identity(identity_id: int):
    return await forward_request("identity", f"/api/identities/{identity_id}", "GET")

@app.get("/gateway/identities/nic/{nic}", dependencies=[Depends(security)])
async def get_identity_by_nic(nic: str):
    return await forward_request("identity", f"/api/identities/nic/{nic}", "GET")

@app.post("/gateway/identities", dependencies=[Depends(security)])
async def create_identity(request: Request):
    body = await request.json()
    return await forward_request("identity", "/api/identities", "POST", json=body)

@app.put("/gateway/identities/{identity_id}", dependencies=[Depends(security)])
async def update_identity(identity_id: int, request: Request):
    body = await request.json()
    return await forward_request("identity", f"/api/identities/{identity_id}", "PUT", json=body)

@app.delete("/gateway/identities/{identity_id}", dependencies=[Depends(security)])
async def delete_identity(identity_id: int):
    return await forward_request("identity", f"/api/identities/{identity_id}", "DELETE")

# -------------------------
# E-Locker Routes (Member 2)
# -------------------------
@app.get("/gateway/documents", dependencies=[Depends(security)])
async def get_all_documents():
    return await forward_request("elocker", "/api/documents", "GET")

@app.get("/gateway/documents/{citizen_id}", dependencies=[Depends(security)])
async def get_documents_by_citizen(citizen_id: str):
    return await forward_request("elocker", f"/api/documents/{citizen_id}", "GET")

@app.get("/gateway/documents/{citizen_id}/{doc_id}", dependencies=[Depends(security)])
async def get_document(citizen_id: str, doc_id: int):
    return await forward_request("elocker", f"/api/documents/{citizen_id}/{doc_id}", "GET")

@app.post("/gateway/documents/upload", dependencies=[Depends(security)])
async def upload_document(request: Request):
    body = await request.json()
    return await forward_request("elocker", "/api/documents/upload", "POST", json=body)

@app.put("/gateway/documents/{doc_id}", dependencies=[Depends(security)])
async def update_document(doc_id: int, request: Request):
    body = await request.json()
    return await forward_request("elocker", f"/api/documents/{doc_id}", "PUT", json=body)

@app.delete("/gateway/documents/{doc_id}", dependencies=[Depends(security)])
async def delete_document(doc_id: int):
    return await forward_request("elocker", f"/api/documents/{doc_id}", "DELETE")

# -------------------------
# GovPay Routes (Member 3)
# -------------------------
@app.get("/gateway/payments", dependencies=[Depends(security)])
async def get_all_payments():
    return await forward_request("govpay", "/api/payments", "GET")

@app.get("/gateway/payments/history/{citizen_id}", dependencies=[Depends(security)])
async def get_payment_history(citizen_id: str):
    return await forward_request("govpay", f"/api/payments/history/{citizen_id}", "GET")

@app.get("/gateway/payments/{payment_id}", dependencies=[Depends(security)])
async def get_payment(payment_id: str):
    return await forward_request("govpay", f"/api/payments/{payment_id}", "GET")

@app.post("/gateway/payments/create", dependencies=[Depends(security)])
async def create_payment(request: Request):
    body = await request.json()
    return await forward_request("govpay", "/api/payments/create", "POST", json=body)

@app.post("/gateway/payments/refund", dependencies=[Depends(security)])
async def refund_payment(request: Request):
    body = await request.json()
    return await forward_request("govpay", "/api/payments/refund", "POST", json=body)

@app.delete("/gateway/payments/{payment_id}", dependencies=[Depends(security)])
async def delete_payment(payment_id: str):
    return await forward_request("govpay", f"/api/payments/{payment_id}", "DELETE")

# -------------------------
# Error handler
# -------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "path": str(request.url)}
    )

# -------------------------
# Beneficiary Routes (Member 4)
class ProgramEnum(str, Enum):
    ASWESUMA = "Aswesuma"
    SAMURDHI = "Samurdhi"
    ELDERLY_SUPPORT = "Elderly Support"


class IncomeLevelEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class BeneficiaryCreateGateway(BaseModel):
    citizen_id: str
    program: ProgramEnum
    income_level: IncomeLevelEnum


class BeneficiaryUpdateGateway(BaseModel):
    program: Optional[ProgramEnum] = None
    income_level: Optional[IncomeLevelEnum] = None


# -------------------------
@app.get("/gateway/beneficiary/list", dependencies=[Depends(security)])
async def get_all_beneficiaries():
    return await forward_request("beneficiary", "/api/beneficiary/list", "GET")

@app.get("/gateway/beneficiary/{citizen_id}", dependencies=[Depends(security)])
async def get_beneficiary_by_citizen_id(citizen_id: str):
    return await forward_request("beneficiary", f"/api/beneficiary/{citizen_id}", "GET")

@app.post("/gateway/beneficiary/apply", dependencies=[Depends(security)])
async def apply_for_beneficiary(beneficiary_data: BeneficiaryCreateGateway):
    return await forward_request(
        "beneficiary",
        "/api/beneficiary/apply",
        "POST",
        json=beneficiary_data.model_dump()
    )

@app.put("/gateway/beneficiary/{citizen_id}", dependencies=[Depends(security)])
async def update_beneficiary(citizen_id: str, beneficiary_data: BeneficiaryUpdateGateway):
    return await forward_request(
        "beneficiary",
        f"/api/beneficiary/{citizen_id}",
        "PUT",
        json=beneficiary_data.model_dump(exclude_none=True)
    )

@app.delete("/gateway/beneficiary/{id}", dependencies=[Depends(security)])
async def delete_beneficiary(id: int):
    return await forward_request("beneficiary", f"/api/beneficiary/{id}", "DELETE")