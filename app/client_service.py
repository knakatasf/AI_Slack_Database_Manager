from typing import List
from client_repository import ClientRepository
from client_dao import ClientDAO
from schema import ClientSchema


class ClientService:
    ALLOWED = ["name", "address", "email_address", "phone_number"]

    def __init__(self, repo: ClientRepository):
        self.repo = repo
        self.find_map = {
            "name": self.repo.find_by_name,
            "address": self.repo.find_by_address,
            "email_address": self.repo.find_by_email_address,
            "phone_number": self.repo.find_by_phone_number
        }

    def insert_client(self, client_schema: ClientSchema) -> ClientDAO:
        if not client_schema.name or not client_schema.address \
                or not client_schema.email_address or not client_schema.phone_number:
            raise ValueError("All the fields are required")

        return self.repo.insert(
            name=client_schema.name,
            address=client_schema.address,
            email_address=client_schema.email_address,
            phone_number=client_schema.phone_number
        )

    def find_client(self, search_field, search_value) -> List[ClientDAO]:
        if search_field not in self.ALLOWED:
            raise ValueError(f"Invalid field {search_field}; must be one of {self.ALLOWED}")

        func = self.find_map.get(search_field, self._find_error)
        return func(search_value)

    def _find_error(self, search_value) -> str:
        message = f"Invalid field name returned from the AI: {search_value}"
        return message

    def update_client(self, id: int, update_field: str, update_value: str) -> ClientDAO:
        if update_field not in self.ALLOWED:
            raise ValueError(f"Invalid field {update_field}; must be one of {self.ALLOWED}")

        return self.repo.update(id, update_field, update_value)