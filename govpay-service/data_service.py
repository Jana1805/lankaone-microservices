from typing import List, Optional
from model import Payment, PaymentCreate, PaymentUpdate


class PaymentMockDataService:
    def __init__(self):
        self._payments: List[Payment] = [
            Payment(
                id=1,
                payment_id="PAY10001",
                citizen_id="SLUDI10001",
                payment_type="Electricity Bill",
                amount=3500.0,
                method="Card",
                status="SUCCESS",
            ),
            Payment(
                id=2,
                payment_id="PAY10002",
                citizen_id="SLUDI10002",
                payment_type="Water Bill",
                amount=1200.0,
                method="Mobile Pay",
                status="SUCCESS",
            ),
            Payment(
                id=3,
                payment_id="PAY10003",
                citizen_id="SLUDI10001",
                payment_type="Tax",
                amount=25000.0,
                method="Bank Transfer",
                status="PENDING",
            ),
        ]
        self._next_id = 4
        self._next_pay_num = 10004  # Next payment_id number

    def _generate_payment_id(self) -> str:
        pay_id = f"PAY{self._next_pay_num}"
        self._next_pay_num += 1
        return pay_id

    def get_all(self) -> List[Payment]:
        return self._payments

    def get_by_payment_id(self, payment_id: str) -> Optional[Payment]:
        for p in self._payments:
            if p.payment_id == payment_id:
                return p
        return None

    def get_by_citizen_id(self, citizen_id: str) -> List[Payment]:
        return [p for p in self._payments if p.citizen_id == citizen_id]

    def create(self, data: PaymentCreate) -> Payment:
        payment = Payment(
            id=self._next_id,
            payment_id=self._generate_payment_id(),
            citizen_id=data.citizen_id,
            payment_type=data.payment_type,
            amount=data.amount,
            method=data.method,
            status="PENDING",
        )
        self._next_id += 1
        self._payments.append(payment)
        # Simulate processing: mark as SUCCESS immediately
        payment.status = "SUCCESS"
        return payment

    def update(self, payment_id: str, data: PaymentUpdate) -> Optional[Payment]:
        for p in self._payments:
            if p.payment_id == payment_id:
                if data.status is not None:
                    p.status = data.status
                if data.amount is not None:
                    p.amount = data.amount
                return p
        return None

    def refund(self, payment_id: str) -> Optional[Payment]:
        for p in self._payments:
            if p.payment_id == payment_id:
                p.status = "REFUNDED"
                return p
        return None

    def delete(self, payment_id: str) -> bool:
        for i, p in enumerate(self._payments):
            if p.payment_id == payment_id:
                self._payments.pop(i)
                return True
        return False