from telethon import TelegramClient, events
import yaml
from signal_parser import extract_signal
from executor import place_trade
from dotenv import load_dotenv
import os

# Load config and env
load_dotenv()
with open("config/presets.yaml", "r") as f:
    presets = yaml.safe_load(f)

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
channel_username = 'YourSignalChannelUsername'  # <- update this

client = TelegramClient('session', api_id, api_hash)

def should_parse(msg):
    return any(x in msg.lower() for x in ["entry", "tp", "sl", "target"])

def clean_text(text):
    return text.replace("📩", "").replace("💡", "").replace("🎯", "").strip()

@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    text = event.raw_text
    if should_parse(text):
        print(f"\n📨 New Signal Received:\n{text[:200]}...\n")
        try:
            parsed = extract_signal(clean_text(text))
            place_trade(parsed, presets)
        except Exception as e:
            print(f"❌ Error handling signal: {e}")

def main():
    print("✅ Live bot running and listening for signals...\n")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
