import os
import openai
from slack_bolt import App, Respond, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/capyoftheday")
def dailycapy_command(ack, say: Say):
    ack()

    url = "https://api.capy.lol/v1/capyoftheday?json=true"
    response = requests.get(url)

    response.raise_for_status()  # raises exception when not a 2xx response
    response_json = ''
    if response.status_code != 204:
        response_json = response.json()

    response_json = response.json()
    if response_json != '' and response_json["success"]:
        print("Sending capy of the day")
        data = response_json["data"]
        print(data)
        say(
            blocks = [
                {
                "type": "image",
                "image_url": data["url"],
                "alt_text": data["alt"]
                }
            ]
        )
    else:
        say("Daily Capy failed. Try again later.")


@app.event("app_mention")
def event_mention(event, say: Say):
    say(get_answer(event["text"]))


def get_answer(message):
    openai.organization = os.getenv("OPENAI_ORGANIZATION")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful and friendly capybara assistant for Team Capybara."
            },
            {
                "role": "user", 
                "content": message
            }
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

