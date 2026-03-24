# identity-service/data_service.py
from model import Identity


class IdentityMockDataService:
    def __init__(self):
        self.identities = [
            Identity(id=1, nic="200012345678", name="Kasun Perera",    dob="12-05-2000", biometric_hash="AHD87373HD", status="Verified"),
            Identity(id=2, nic="199856781234", name="Nimali Fernando", dob="03-11-1998", biometric_hash="BKT92810XZ", status="Verified"),
            Identity(id=3, nic="200234569871", name="Ruwan Silva",     dob="19-07-2002", biometric_hash="CLP11234QR", status="Pending"),
        ]
        self.next_id = 4

    def get_all_identities(self):
        return self.identities

    def get_identity_by_id(self, identity_id: int):
        return next((i for i in self.identities if i.id == identity_id), None)

    def get_identity_by_nic(self, nic: str):
        return next((i for i in self.identities if i.nic == nic), None)

    def add_identity(self, identity_data):
        new_identity = Identity(
            id=self.next_id,
            status="Pending",
            **identity_data.dict()
        )
        self.identities.append(new_identity)
        self.next_id += 1
        return new_identity

    def update_identity_by_nic(self, nic: str, identity_data):
        identity = self.get_identity_by_nic(nic)
        if identity:
            update_data = identity_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(identity, key, value)
            return identity
        return None

    def delete_identity_by_nic(self, nic: str):
        identity = self.get_identity_by_nic(nic)
        if identity:
            self.identities.remove(identity)
            return True
        return False