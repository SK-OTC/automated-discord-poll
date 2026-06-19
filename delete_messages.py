import os
import sys
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

import requests

load_dotenv()

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = os.environ["DISCORD_CHANNEL_ID"]
BASE = "https://discord.com/api/v10"
HEADERS = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

# Safety guard: never delete a message younger than this many hours,
# so a still-running poll can't be removed even if timing slips.
MIN_AGE_HOURS = 8

def get(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def message_age_hours(msg):
    ts = datetime.fromisoformat(msg["timestamp"])  # Discord returns ISO8601 w/ offset
    return (datetime.now(timezone.utc) - ts).total_seconds() / 3600

def delete_message(message_id):
    r = requests.delete(f"{BASE}/channels/{CHANNEL_ID}/messages/{message_id}",
                        headers=HEADERS, timeout=30)
    if r.status_code == 429:  # rate limited
        time.sleep(r.json().get("retry_after", 1) + 0.5)
        return delete_message(message_id)
    if not r.ok:
        print(f"Failed to delete {message_id}: {r.status_code} {r.text}", file=sys.stderr)
        return False
    return True

def main():
    bot_id = get(f"{BASE}/users/@me")["id"]
    messages = get(f"{BASE}/channels/{CHANNEL_ID}/messages?limit=50")

    targets = [
        m for m in messages
        if m.get("author", {}).get("id") == bot_id
        and message_age_hours(m) >= MIN_AGE_HOURS
    ]

    if not targets:
        print("No eligible bot messages to delete.")
        return

    deleted = 0
    for m in targets:
        if delete_message(m["id"]):
            deleted += 1
            time.sleep(0.4)  # stay gentle on the rate limiter
    print(f"Deleted {deleted} message(s).")

if __name__ == "__main__":
    main()