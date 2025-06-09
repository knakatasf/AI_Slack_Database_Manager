from dotenv import load_dotenv
import os, json

from groq import Groq
from client_service import ClientService
from schema import ClientSchema, SearchSchema, UpdateSchema

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
groq = Groq(api_key=GROQ_API_KEY)

class AIService:
    def __init__(self, client_service: ClientService):
        self.client_service = client_service

    def process(self, user_id: str, user_input: str) -> str:
        operation_type = self._determine_operation_type(user_input)

        try:
            operation_type = int(operation_type)
            if operation_type < 1 or operation_type > 4:
                raise ValueError
        except ValueError:
            print("Groq returned an invalid operation_type: ", operation_type)
            operation_type = 0

        operations = ["dummy", self._handle_add, self._handle_search, "update", "delete"]

        message = operations[operation_type](user_input)
        return message

    def _determine_operation_type(self, user_input: str):
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

    def _handle_add(self, user_input: str):
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

        client_schema = ClientSchema.model_validate_json(chat_completion.choices[0].message.content)
        self.client_service.insert_client(client_schema)

        return f"{client_schema} \nwas added to the database!"

    def _handle_search(self, user_input: str) -> str:
        chat_completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""
                                You are a helper that turns arbitrary user requests into a structured search intent
                                for looking up client records.  
                                Return exactly one JSON object matching this schema: 
                                {json.dumps(SearchSchema.model_json_schema())}
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
        search_schema = SearchSchema.model_validate_json(chat_completion.choices[0].message.content)
        client_list = self.client_service.find_client(search_schema.field, search_schema.value)
        if not client_list:
            return f"Couldn't find clients whose {search_schema.field} is {search_schema.value}.."

        return "\n".join([str(client) for client in client_list])

    def _handle_update(self, user_input: str) -> str:
        chat_completion = groq.chat.completions.create(
            messages=[
                {"role": "system",
                 "content": f"""
                            You are an intent extractor. From the user’s request, 
                            output exactly one JSON object matching this JSON Schema:
                            {json.dumps(UpdateSchema.model_json_schema(), indent=2)}
                            Return only the JSON object—no extra text or markdown.
                            Example:
                            {{
                                "search_field": "name",
                                "search_value": "Koichi Nakata",
                                "update_field":"address",
                                "update_value": "Los Angeles"
                            }}
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
        update_schema = UpdateSchema.model_validate_json(chat_completion.choices[0].message.content)

        search_field, search_value = update_schema.search_field, update_schema.search_value
        update_field, update_value = update_schema.update_field, update_schema.update_value

        matched_clients = self.client_service.find_client(search_field, search_value)
        if not matched_clients:
            return f"No clients found for {search_field} = {search_value}.."

        self._pending_update[current_user] = {
            "matched_client": matched_clients,
            "update_field": update_field,
            "update_value": update_value
        }

        clients_list = [f"{i + 1}: {str(client)}" for i, client in matched_clients]
        return ("I found those clients matched:\n" +
                "\n".join(clients_list) +
                "\nPlease reply with the number of the client you wanted to update")