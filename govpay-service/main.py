from fastapi import FastAPI, HTTPException, status
from model import Payment, PaymentCreate, PaymentUpdate
from service import PaymentService
from pydantic import BaseModel

app = FastAPI(
    title="GovPay Service",
    description="LankaOne – Government Payment Processing Microservice",
    version="1.0.0",
)

payment_service = PaymentService()


# ── Request body for refund ───────────────────────────────────────────────────
class RefundRequest(BaseModel):
    payment_id: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def read_root():
    return {"message": "GovPay Service is running", "port": 8083}

@app.get(
    "/api/payments",
    response_model=list[Payment],
    status_code=status.HTTP_200_OK,
    summary="Get all payments",
)
def get_all_payments():
    return payment_service.get_all_payments()


@app.get(
    "/api/payments/{payment_id}",
    response_model=Payment,
    status_code=status.HTTP_200_OK,
    summary="Get payment by payment ID",
)
def get_payment(payment_id: str):
    payment = payment_service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID '{payment_id}' not found.",
        )
    return payment


@app.get(
    "/api/payments/history/{citizen_id}",
    response_model=list[Payment],
    status_code=status.HTTP_200_OK,
    summary="Get payment history for a citizen",
)
def get_payment_history(citizen_id: str):
    history = payment_service.get_payment_history(citizen_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No payment records found for citizen '{citizen_id}'.",
        )
    return history


@app.post(
    "/api/payments/create",
    response_model=Payment,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new payment",
)
def create_payment(data: PaymentCreate):
    return payment_service.create_payment(data)


@app.post(
    "/api/payments/refund",
    response_model=Payment,
    status_code=status.HTTP_200_OK,
    summary="Refund a payment (change status to REFUNDED)",
)
def refund_payment(body: RefundRequest):
    payment = payment_service.refund_payment(body.payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID '{body.payment_id}' not found.",
        )
    return payment


@app.delete(
    "/api/payments/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a payment record",
)
def delete_payment(payment_id: str):
    deleted = payment_service.delete_payment(payment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID '{payment_id}' not found.",
        )

