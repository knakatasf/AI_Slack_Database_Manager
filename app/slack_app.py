from dotenv import load_dotenv
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from groq import Groq
from database import SessionLocal
from client_repository import ClientRepository
from client_service import ClientService
from ai_service import AIService

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()

app = App(token=SLACK_BOT_TOKEN)
groq = Groq(api_key=GROQ_API_KEY)

session = SessionLocal()
client_repo = ClientRepository(session)
client_service = ClientService(client_repo)
ai_service = AIService(client_service)


@app.event("app_mention")
def respond(event, say):
    user_id = event["user"]
    user_input = event["text"]
    message = ai_service.process(user_id, user_input)

    say(f"Hi <@{user_id}>, I'm an AI Database Manager! \n{message}")


if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()