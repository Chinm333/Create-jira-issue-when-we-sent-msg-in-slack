import requests
from requests.auth import HTTPBasicAuth
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

# load_dotenv will load our environment file
# create_issue using automation url which is putted in the jira webhook


def create_issue():
    response = requests.request("POST", url="AUTOMATION_JIRA_WEBHOOK",
                                auth=HTTPBasicAuth("MAIL", "JIRA_PROJECT_API"))
    return response
# create_issue()


env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']
# giving us the id of the bot
@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    user_id = event.get('user')
    if BOT_ID!= user_id:
        client.chat_postMessage(channel='#practice',text=f'Issue created and your response is {create_issue()}')
if __name__ == "__main__":
    app.run(debug=True)
