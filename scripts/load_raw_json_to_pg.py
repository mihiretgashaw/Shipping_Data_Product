import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

conn = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    database="telegram_db",
    user="postgres",
    password="admin"
)
cur = conn.cursor()

data_folder = Path("data/raw/telegram_messages/2025-07-11") 

for json_file in data_folder.glob("*.json"):
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
            msg["id"],
            msg["date"],
            msg["sender_id"],
            msg["message"],
            msg["media"]
        ))

conn.commit()
cur.close()
conn.close()
