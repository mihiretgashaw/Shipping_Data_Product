# my_project/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopProduct(BaseModel):
    product_name: str
    mention_count: int

class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int
    last_posted_at: Optional[datetime]

class Message(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    message_timestamp: datetime
