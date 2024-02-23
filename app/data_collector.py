from telethon import TelegramClient
from telethon.types import Channel as TGChannel
from telethon.tl.functions.channels import GetFullChannelRequest
import datetime
from app.database.models import Channel as DBChannel
from app.database.requests import add_channel_data
from config import API_HASH, API_ID, CLIENT_PHONE

collector = TelegramClient("collector_session", api_id=API_ID, api_hash=API_HASH).start(
    CLIENT_PHONE
)


async def collect_from_link(link):
    channel = await collector.get_entity(link)
    part_count = (
        await collector(GetFullChannelRequest(channel))
    ).full_chat.participants_count
    first_message = (
        await collector.get_messages(channel, limit=1, min_id=0, reverse=True)
    )[0]
    posts7 = 0
    views7 = 0
    async for post in collector.iter_messages(
        channel,
        offset_date=datetime.datetime.now() - datetime.timedelta(days=7),
        reverse=True,
    ):
        posts7 += 1
        if post.views is not None:
            views7 += post.views

    out = DBChannel(link, first_message.date.date(), part_count, posts7, views7)
    await add_channel_data(out)
