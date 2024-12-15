import os
import requests
import json
from datetime import datetime

# Environment variables - replace with your actual values!
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # your bot token
CHANNEL_ID = os.getenv("CHANNEL_ID") # id of channel that has the attachment
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # your webhook url
STATE_FILE = "processed_messages.json" # Local file to keep track of processed messages

def load_processed_messages():
    try:
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_processed_messages(processed_ids):
    with open(STATE_FILE, "w") as f:
        json.dump(list(processed_ids), f)

def fetch_messages(last_id=None):
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}"
    }
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    params = {"limit": 100}  # Adjust the limit as needed
    if last_id:
        params["after"] = last_id
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def process_messages(processed_ids):
    messages = fetch_messages()
    if not messages:
      print("No messages retrieved.")
      return False
    new_messages_found = False
    for message in messages:
        if message["id"] not in processed_ids:
            if message.get("attachments"):
               for attachment in message["attachments"]:
                 if attachment["filename"].endswith((".yaml", ".yml", ".sh", ".py", ".txt", ".json", ".lua")):
                   post_to_webhook(attachment["url"])
                   new_messages_found = True
            processed_ids.add(message["id"])
    return new_messages_found

def post_to_webhook(url):
    payload = {
      "content": f"New script uploaded: {url} at {datetime.now()}"
    }
    response = requests.post(WEBHOOK_URL, json=payload)
    response.raise_for_status()
    print("posted:", url)
    

if __name__ == "__main__":
    processed_ids = load_processed_messages()
    new_messages_found = process_messages(processed_ids)
    if new_messages_found:
        save_processed_messages(processed_ids)
    else:
        print("No new script attachments found.")
