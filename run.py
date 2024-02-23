from app.bot_handlers import start
from app.database.requests import create_tables
from datetime import date
import asyncio


async def main():
    await create_tables()
    await start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
