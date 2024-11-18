from dotenv import load_dotenv
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from groq import Groq

import ai_service
import db_manager

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()

app = App(token=SLACK_BOT_TOKEN)
groq = Groq(api_key=GROQ_API_KEY)

@app.event("app_mention")
def respond(event, say):
    user_id = event["user"]
    user_input = event["text"]
    client = ai_service.analyze_input(user_input)

    say(f"Hi <@{user_id}>, I'm a Slack Bot! This is what I extracted: \n{client}")


if __name__ == '__main__':
    db_manager.connect()
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

