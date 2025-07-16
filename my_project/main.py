from fastapi import FastAPI, HTTPException, Query
from typing import List
from my_project.schemas import TopProduct, ChannelActivity, Message
from my_project.crud import get_top_products, get_channel_activity, search_messages
from my_project.database import connect, disconnect

app = FastAPI(title="Analytical API")

@app.on_event("startup")
async def startup():
    await connect()

@app.on_event("shutdown")
async def shutdown():
    await disconnect()

@app.get("/api/reports/top-products", response_model=List[TopProduct])
async def top_products(limit: int = Query(10, ge=1, le=100)):
    results = await get_top_products(limit)
    return results

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
async def channel_activity(channel_name: str):
    result = await get_channel_activity(channel_name)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result

@app.get("/api/search/messages", response_model=List[Message])
async def search_messages_endpoint(query: str = Query(..., min_length=1)):
    results = await search_messages(query)
    return results
