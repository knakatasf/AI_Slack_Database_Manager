from dotenv import load_dotenv
import os
import json

from pydantic import BaseModel
from groq import Groq

import db_manager

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
groq = Groq(api_key=GROQ_API_KEY)


class Client(BaseModel):
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


SYSTEM_PROMPT = f"""
From the user input, determine which operation the user wants to execute from the following:
(1) Insert a new client to the database.
(2) Search for the client in the database.
(3) Update the client's information in the database.
(4) Delete the client from the database.

Extract the necessary client information and respond in JSON.
The JSON object must use the schema: {json.dumps(Client.model_json_schema())}
"""


def determine_operation_type(user_input: str) -> str:
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    Based on the user's natural language input, determine which database operation they want to perform:
                    1. Insert a new client
                    2. Search for a client
                    3. Update client information
                    4. Delete a client
                    
                    Response format:
                    - If the operation is clear: Only return the corresponding number (1-4)
                    - If unclear/ambiguous: Only return 0
                    """
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
    )
    return chat_completion.choices[0].message.content


def analyze_input(user_input: str):
    operation_type = determine_operation_type(user_input)

    try:
        operation_type = int(operation_type)
    except ValueError:
        print("Groq returned an invalid operation_type: ", operation_type)
        operation_type = 0

    operations = ["dummy", add_operation, "search", "update", "delete"]

    client = operations[operation_type](user_input)
    return client

def add_operation(user_input: str):
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                            Extract the necessary client information and respond in JSON.
                            The JSON object must use the schema: {json.dumps(Client.model_json_schema())}
                            If there is a field not provided in the input, fill it with 'not provided'. 
                            """
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama3-8b-8192",
        temperature=0,
        stream=False,
        response_format={"type": "json_object"}
    )

    return Client.model_validate_json(chat_completion.choices[0].message.content)

