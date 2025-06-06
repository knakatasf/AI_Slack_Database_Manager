from sqlalchemy.orm import Session
from ai_service import ClientSchema
from model import ClientDAO


class ClientRepository:
    def __init__(self, session: Session):
        self.db = session

    def insert(self, name: str, address: str, email_address: str, phone_number: str) -> ClientDAO:
        client_dao = ClientDAO(
            name=name,
            address=address,
            email_address=email_address,
            phone_number=phone_number
        )
        self.db.add(client_dao)
        self.db.commit()
        self.db.refresh(client_dao)
        return client_dao

    def find_by_id(self, id: int) -> ClientDAO:
        return self.db.query(ClientDAO).get(id)

    def find_by_name(self, name: str) -> [ClientDAO]:
        return self.db.query(ClientDAO).filter(ClientDAO.name == name)

    def find_by_address(self, address: str) -> [ClientDAO]:
        return self.db.query(ClientDAO).filter(ClientDAO.address == address)

    def find_by_email_address(self, email_address: str) -> [ClientDAO]:
        return self.db.query(ClientDAO).filter(ClientDAO.email_address == email_address)

    def find_by_phone_number(self, phone_number: str) -> [ClientDAO]:
        return self.db.query(ClientDAO).filter(ClientDAO.phone_number == phone_number)
