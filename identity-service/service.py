# identity-service/service.py
from data_service import IdentityMockDataService


class IdentityService:
    def __init__(self):
        self.data_service = IdentityMockDataService()

    def get_all(self):
        return self.data_service.get_all_identities()

    def get_by_id(self, identity_id: int):
        return self.data_service.get_identity_by_id(identity_id)

    def get_by_nic(self, nic: str):
        return self.data_service.get_identity_by_nic(nic)

    def create(self, identity_data):
        return self.data_service.add_identity(identity_data)

    def update_by_nic(self, nic: str, identity_data):
        return self.data_service.update_identity_by_nic(nic, identity_data)

    def delete_by_nic(self, nic: str):
        return self.data_service.delete_identity_by_nic(nic)