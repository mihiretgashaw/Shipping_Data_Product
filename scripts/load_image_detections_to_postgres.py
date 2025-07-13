import psycopg2
import pandas as pd

df = pd.read_csv("data/processed/image_detections.csv")

conn = psycopg2.connect(
    dbname="telegram_db",
    user="postgres",
    password="admin",
    host="localhost",
    port=5433
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS raw.image_detections (
    message_id TEXT,
    file_name TEXT,
    object_class TEXT,
    confidence_score FLOAT
)
""")
conn.commit()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO raw.image_detections (message_id, file_name, object_class, confidence_score)
        VALUES (%s, %s, %s, %s)
    """, (row.message_id, row.file_name, row.object_class, row.confidence_score))

conn.commit()
cur.close()
conn.close()
