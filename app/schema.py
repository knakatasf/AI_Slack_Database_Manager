from typing import Literal
from pydantic import BaseModel, Field

AllowedField = Literal["name", "address", "email_address", "phone_number"]

class ClientSchema(BaseModel):
    name: str
    address: str
    email_address: str
    phone_number: str

    def __str__(self):
        return f"""
        Client: {self.name}
        Address: {self.address}
        Email Address: {self.email_address}
        Phone: {self.phone_number}
        """


class SearchSchema(BaseModel):
    field: AllowedField = Field(..., description="Which client field to search by")
    value: str = Field(..., description="The exact text to search for")


class UpdateSchema(BaseModel):
    search_field: AllowedField = Field(..., description="Which client field to search by")
    search_value: str = Field(..., description="The exact text to search for")
    update_field: AllowedField = Field(..., description="Which client field to update")
    update_value: str = Field(..., description="The new value to set for the update field")

