import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import ChannelInvalidError
import traceback

# Load secrets
load_dotenv()
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

# Validate credentials
if not api_id or not api_hash:
    raise EnvironmentError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")
api_id = int(api_id)

# Telegram Channels
CHANNELS = {
    "lobelia4cosmetics": "https://t.me/lobelia4cosmetics",
    "tikvahpharma": "https://t.me/tikvahpharma",
    "chemed": "https://t.me/chemed"
}

# Setup logging
logging.basicConfig(
    filename="scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def scrape_channels():
    today = datetime.now().strftime("%Y-%m-%d")
    base_path = Path(f"data/raw/telegram_messages/{today}")
    base_path.mkdir(parents=True, exist_ok=True)

    results = {}

    with TelegramClient("scraper_session", api_id, api_hash) as client:
        for name, url in CHANNELS.items():
            messages_data = []
            try:
                logging.info(f"Scraping channel: {name}")
                for message in client.iter_messages(url, limit=200):
                    msg = {
                        "id": message.id,
                        "date": str(message.date),
                        "sender_id": message.sender_id,
                        "message": message.message,
                        "media": None,
                    }

                    # Save image if present
                    if message.photo:
                        media_path = base_path / f"{name}_{message.id}.jpg"
                        client.download_media(message, file=media_path)
                        msg["media"] = str(media_path)

                    messages_data.append(msg)

                # Save messages to JSON
                file_path = base_path / f"{name}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(messages_data, f, ensure_ascii=False, indent=2)

                logging.info(f"✅ Saved {len(messages_data)} messages for {name} → {file_path}")
                results[name] = len(messages_data)

            except ChannelInvalidError:
                logging.error(f"❌ Invalid channel URL: {url}")
                results[name] = 0
            except Exception as e:
                logging.error(f"❌ Error scraping {name}: {str(e)}\n{traceback.format_exc()}")
                results[name] = 0

    return results


if __name__ == "__main__":
    scrape_results = scrape_channels()
    print(f"Scraping completed: {scrape_results}")
