from dotenv import load_dotenv
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from groq import Groq

from app import ai_service

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

app = App(token=SLACK_BOT_TOKEN)
groq = Groq(api_key=GROQ_API_KEY)

@app.event("app_mention")
def respond(event, say):
    user_id = event["user"]
    user_input = event["text"]
    message = ai_service.analyze_input(user_input)

    say(f"Hi <@{user_id}>, I'm an AI Database Manager! \n{message}")

if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()






