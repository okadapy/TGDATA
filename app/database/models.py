from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import String, Date, DateTime
from typing import Optional
from sqlalchemy import func
from datetime import date, timedelta


class AsyncBase(DeclarativeBase, AsyncAttrs):
    pass


class Channel(AsyncBase):
    __tablename__ = "channel_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[String] = mapped_column(String, nullable=False, unique=True)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    subs_count: Mapped[int] = mapped_column(nullable=False)
    posts7: Mapped[int] = mapped_column(nullable=False)
    viewsM7: Mapped[int] = mapped_column(nullable=False)
    ER: Mapped[float] = mapped_column(nullable=False)
    created: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=func.now()
    )
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def __init__(
        self, link: str, date_of_birth: date, subs_count: int, posts7: int, views7: int
    ):
        viewsM7 = int(views7 / posts7)
        ER = viewsM7 / subs_count * 100

        self.link = link
        self.date_of_birth = date_of_birth
        self.age = (date.today() - self.date_of_birth).days
        self.subs_count = subs_count
        self.posts7 = posts7
        self.viewsM7 = viewsM7
        self.ER = ER

    async def to_string(self) -> str:
        return (
            f"<b>DOB</b>: {self.date_of_birth} "
            f"<b>Age</b> {self.age}\n"
            f"<b>Subs</b> {self.subs_count} "
            f"<b>Posts7</b> {self.posts7} "
            f"<b>ViewsM7</b> {self.viewsM7}\n"
            f"<b>ER</b> {round(self.ER, 2)}% "
        )
