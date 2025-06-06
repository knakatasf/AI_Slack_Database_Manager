from dotenv import load_dotenv
import os
import json

from pydantic import BaseModel, Field
from groq import Groq
from client_controller import ClientController
from client_dao import ClientDAO

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
groq = Groq(api_key=GROQ_API_KEY)


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


class ClientSearch(BaseModel):
    # 1=name, 2=address, 3=email, 4=phone
    field: int = Field(..., description="Which client attribute to search by")
    query: str = Field(..., description="The user’s search text")


def determine_operation_type(user_input: str) -> str:
    chat_completion = groq.chat.completions.create(
        messages = [
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


def add_operation(user_input: str):
    chat_completion = groq.chat.completions.create(
        messages=[
            {
               "role": "system",
                "content": f"""
                        Extract the necessary client information and respond in JSON.
                        The JSON object must use the schema: {json.dumps(ClientSchema.model_json_schema())}
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

    client = ClientSchema.model_validate_json(chat_completion.choices[0].message.content)
    client_controller = ClientController()
    client_controller.add_client(ClientDAO(
        name=client.name,
        address=client.address,
        email_address=client.email_address,
        phone_number=client.phone_number
    ))

    message = f"{client} \nwas added to the database!"
    return message


def search_operation(user_input: str):
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                            You are a helper that turns arbitrary user requests into a structured search intent
                            for looking up client records.  
                            (1) Map the user’s intent to one of these fields (choose exactly one):  
                                1 = name  
                                2 = address  
                                3 = email address  
                                4 = phone number  
                            (2) Extract the search text.
                            The JSON object must use the schema: {json.dumps(ClientSearch.model_json_schema())}
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

    client_search = ClientSearch.model_validate_json(chat_completion.choices[0].message.content)
    client_controller = ClientController()
    clients_str = client_controller.search_client(
        field=client_search.field,
        query=client_search.query
    )

    message = f"Found these clients in the database:\n{clients_str}"
    return message


def analyze_input(user_input: str):
    operation_type = determine_operation_type(user_input)

    try:
        operation_type = int(operation_type)
        if operation_type < 1 or operation_type > 4:
            raise ValueError
    except ValueError:
        print("Groq returned an invalid operation_type: ", operation_type)
        operation_type = 0

    operations = ["dummy", add_operation, search_operation, "update", "delete"]

    message = operations[operation_type](user_input)
    return message