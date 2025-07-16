# my_project/crud.py


from .database import database



async def get_top_products(limit: int = 10):
    query = """
    SELECT product_name, mention_count
    FROM analytics.top_products -- replace with your actual model/table
    ORDER BY mention_count DESC
    LIMIT :limit
    """
    return await database.fetch_all(query=query, values={"limit": limit})

async def get_channel_activity(channel_name: str):
    query = """
    SELECT channel_name, COUNT(*) AS message_count, MAX(message_timestamp) AS last_posted_at
    FROM analytics.fct_messages -- replace with your actual model/table
    WHERE channel_name = :channel_name
    GROUP BY channel_name
    """
    return await database.fetch_one(query=query, values={"channel_name": channel_name})

async def search_messages(keyword: str):
    query = """
    SELECT message_id, channel_name, message_text, message_timestamp
    FROM analytics.fct_messages
    WHERE message_text ILIKE '%' || :keyword || '%'
    ORDER BY message_timestamp DESC
    LIMIT 50
    """
    return await database.fetch_all(query=query, values={"keyword": keyword})
