import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

print("✅ Script started")

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    database="telegram_db",
    user="postgres",
    password="admin"
)
cur = conn.cursor()

data_folder = Path("data/raw/telegram_messages/2025-07-11")

if not data_folder.exists():
    print(f"❌ Data folder not found: {data_folder.resolve()}")
else:
    for json_file in data_folder.glob("*.json"):
        print(f"📂 Processing file: {json_file.name}")
        channel_name = json_file.stem
        with open(json_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        for msg in messages:
            cur.execute("""
                INSERT INTO raw.telegram_messages (channel_name, message_id, message_date, sender_id, message_text, media_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel_name, message_id) DO NOTHING;
            """, (
                channel_name,
                msg.get("id"),
                msg.get("date"),
                msg.get("sender_id"),
                msg.get("message"),
                msg.get("media")
            ))
        print(f"✅ Inserted {len(messages)} messages from {channel_name}")

conn.commit()
cur.close()
conn.close()

print("✅ Script completed")
