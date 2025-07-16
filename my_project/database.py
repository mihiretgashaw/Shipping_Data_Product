# my_project/database.py

from databases import Database

DATABASE_URL = "postgresql://postgres:admin@localhost:5433/telegram_db"

database = Database(DATABASE_URL)

async def connect():
    await database.connect()

async def disconnect():
    await database.disconnect()
