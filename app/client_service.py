from client_repository import ClientRepository
from ai_service import ClientSchema


class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def insert_client(self, client_schema: ClientSchema):
        if not client_schema.name or not client_schema.address \
                or client_schema.email_address or not client_schema.phone_number:
            raise ValueError("All the fields are required")

        return self.repo.insert(
            name=client_schema.name,
            address=client_schema.address,
            email_address=client_schema.email_address,
            phone_number=client_schema.phone_number
        )
