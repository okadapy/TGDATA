from app.database.models import AsyncBase, Channel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from config import DB_URL

_engine = create_async_engine(DB_URL, echo=True)
_sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)


async def create_tables():
    async with _engine.begin() as connection:
        await connection.run_sync(AsyncBase.metadata.create_all)


async def add_channel_data(channel: Channel):
    async with _sessionmaker() as session:
        async with session.begin():
            try:
                session.add(channel)
            except IntegrityError:
                await session.rollback()
                await update_channel_data(channel)


async def update_channel_data(new_data: Channel):
    update_stmt = (
        update(Channel)
        .where(Channel.link == new_data.link)
        .values(
            subs_count=new_data.subs_count,
            posts7=new_data.posts7,
            viewsM7=new_data.viewsM7,
        )
    )
    async with _sessionmaker() as session:
        async with session.begin():
            await session.execute(update_stmt)


async def get_channel_data(link: str) -> str | None:
    select_stmt = select(Channel).where(Channel.link == link)
    async with _sessionmaker() as session:
        async with session.begin():
            select_stmt_result = await session.execute(select_stmt)
            channel = select_stmt_result.fetchone()
        if channel is None:
            out = None

        else:
            out = await channel.tuple()[0].to_string()

    return out
