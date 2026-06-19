import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.environ.get("DISCORD_CHANNEL_ID")
URL = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
HEADERS = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

poll_payload = {
    "content": "¿Quién practicará hoy? / Who is practicing today?",
    "poll": {
        "question": {"text": "Select all that apply"},
        "answers": [
            {"answer_id": 1, "poll_media": {"text": "Antes de las 5 (UTC-6)/ Before 5pm/17:00 (UTC-6)", "emoji": {"name": "⏪"}}},
            {"answer_id": 2, "poll_media": {"text": "A las 5 (UTC-6) o despues/ 5pm/17:00(UTC-6) or after", "emoji": {"name": "⏩"}}},
            {"answer_id": 3, "poll_media": {"text": "No puedo practicar/ I can't practice", "emoji": {"name": "❌"}}},
            {"answer_id": 4, "poll_media": {"text": "Escucharé/ I'll listen in", "emoji": {"name": "💬"}}},
            {"answer_id": 5, "poll_media": {"text": "Ambos tiempos/ Both times", "emoji": {"name": "🔥"}}},
            {"answer_id": 6, "poll_media": {"text": "No sé/ I dont know", "emoji": {"name": "😭"}}},
        ],
        "allow_multiselect": True,
        "duration": 8,  # hours the poll stays open
    },
}

ping_payload = {
    "content": "@everyone VOTEEEEEEEEEEE",
    "allowed_mentions": {"parse": ["everyone"]},  # required for the ping to fire
}

def post(payload):
    r = requests.post(URL, headers=HEADERS, json=payload, timeout=30)
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        r.raise_for_status()

if __name__ == "__main__":
    post(poll_payload)
    post(ping_payload)
    print("Poll + ping sent.")