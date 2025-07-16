# api/crud.py

import psycopg2
import os

def get_top_products(limit):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT LOWER(word) as product, COUNT(*) as freq
        FROM (
            SELECT unnest(string_to_array(text, ' ')) AS word
            FROM fct_messages
        ) sub
        WHERE word ~ '^[a-zA-Z]+$'
        GROUP BY word
        ORDER BY freq DESC
        LIMIT %s;
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"product": row[0], "count": row[1]} for row in results]
