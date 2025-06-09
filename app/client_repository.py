from typing import List
from sqlalchemy.orm import Session
from client_dao import ClientDAO


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

    def _find_like(self, column, value: str) -> List[ClientDAO]:
        pattern = f"%{value}%"
        return self.db.query(ClientDAO).filter(column.ilike(pattern)).all()

    def find_by_name(self, name: str) -> List[ClientDAO]:
        return self._find_like(ClientDAO.name, name)

    def find_by_address(self, address: str) -> List[ClientDAO]:
        return self._find_like(ClientDAO.address, address)

    def find_by_email_address(self, email_address: str) -> List[ClientDAO]:
        return self._find_like(ClientDAO.email_address, email_address)

    def find_by_phone_number(self, phone_number: str) -> List[ClientDAO]:
        return self._find_like(ClientDAO.phone_number, phone_number)

    def update(self, id: int, update_field: str, update_value: str) -> ClientDAO:
        target_client = self.find_by_id(id)
        if target_client is None:
            raise ValueError(f"No client found with id={id}")

        setattr(target_client, update_field, update_value)

        self.db.commit()
        self.db.refresh()

        return target_client
