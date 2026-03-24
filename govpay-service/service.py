from typing import List, Optional
from model import Payment, PaymentCreate, PaymentUpdate
from data_service import PaymentMockDataService


class PaymentService:
    def __init__(self):
        self._data_service = PaymentMockDataService()

    def get_all_payments(self) -> List[Payment]:
        return self._data_service.get_all()

    def get_payment_by_id(self, payment_id: str) -> Optional[Payment]:
        return self._data_service.get_by_payment_id(payment_id)

    def get_payment_history(self, citizen_id: str) -> List[Payment]:
        return self._data_service.get_by_citizen_id(citizen_id)

    def create_payment(self, data: PaymentCreate) -> Payment:
        return self._data_service.create(data)

    def refund_payment(self, payment_id: str) -> Optional[Payment]:
        return self._data_service.refund(payment_id)

    def delete_payment(self, payment_id: str) -> bool:
        return self._data_service.delete(payment_id)