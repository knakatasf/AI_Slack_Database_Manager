from dotenv import load_dotenv
import os
import json

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from groq import Groq

import CONST

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()

app = App(token=SLACK_BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@app.event("app_mention")
def respond(event, say):
    user_id = event["user"]
    user_input = event["text"]
    json_response = analyze_user_input(user_input)

    print(type(json_response))
    # operation_type = json_response["client_data_analysis"]["operation_type"]
    # client_name = json_response["client_data_analysis"]["client_data"]["name"]
    #say(f"Hi <@{user_id}>, I'm a Slack Bot! I understand you want to do {operation_type} for the client {client_name}")

def analyze_user_input(user_input):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": CONST.SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        model="llama3-8b-8192",
        response_format={"type": "json_object"}
    )
    json_response = response.choices[0].message.content
    return json_response

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
