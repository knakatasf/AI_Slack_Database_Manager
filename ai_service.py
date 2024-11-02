from dotenv import load_dotenv
import os
import json

from pydantic import BaseModel
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
groq = Groq(api_key=GROQ_API_KEY)


class Client(BaseModel):
    operation_type: int
    name: str
    address: str
    email_address: str
    phone_number: str

    def __str__(self):
        return f"""
        Client: {self.name}
        Operation Type: {self.operation_type}
        Address: {self.address}
        Email Address: {self.email_address}
        Phone: {self.phone_number}
        """

SYSTEM_PROMPT = f"""
From the user input, determine which operation the user wants to execute from the following:
(1) Insert a new client to the database.
(2) Search for the client in the database.
(3) Update the client's information in the database.
(4) Delete the client from the database.

Extract the necessary client information and respond in JSON.
The JSON object must use the schema: {json.dumps(Client.model_json_schema())}
"""

def analyze_input(user_input: str) -> Client:
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"},
    )
    return Client.model_validate_json(chat_completion.choices[0].message.content)


def print_client(client: Client):
    print(f"Client: {client.name}")
    print(f"Operation Type: {client.operation_type}")
    print(f"Address: {client.address}")
    print(f"Email Address: {client.email_address}")
    print(f"Phone: {client.phone_number}")
