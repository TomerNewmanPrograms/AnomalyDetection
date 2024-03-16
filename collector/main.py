from fastapi import FastAPI

from collector.collector import create_topic_if_not_exists, list_known_topics, run_collector
from settings import settings
import asyncio

app = FastAPI()


@app.get("/")
async def greeting():
    return {"message": "Hello World!"}


@app.get("/liveness")
async def liveness():
    return {"status": "ok"}


@app.get("/readiness")
async def readiness():
    return {"status": "ready"}


@app.get("/collect")
async def collect():
    await create_topic_if_not_exists(settings.topic)
    await list_known_topics()
    await asyncio.create_task(run_collector())
