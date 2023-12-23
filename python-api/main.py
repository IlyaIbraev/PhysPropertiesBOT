from fastapi import FastAPI
from config_data.config import Config, load_config
from routers import properties
from database.configuring_db import prepare_database
import asyncio

async def main():

    await prepare_database()

asyncio.run(main())

app = FastAPI()
app.include_router(properties.router)