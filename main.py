from dotenv import load_dotenv
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN").strip()
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN").strip()

app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def respond(event, say):
    user_id = event["user"]
    say(f"Hi <@{user_id}>, I'm a Slack Bot!")


if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
