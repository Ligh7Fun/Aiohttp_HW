import datetime
import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv()


PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

PG_DSN = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
)

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "aiohttp_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
    )
    tokens = relationship("Token", back_populates="user")
    ads = relationship("Ads", back_populates="owner")

    @property
    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "registration_time": int(self.registration_time.timestamp()),
        }


class Token(Base):
    __tablename__ = "aiohttp_tokens"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=str(
            uuid.uuid4(),
        ),
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("aiohttp_users.id", ondelete="CASCADE")
    )
    user = relationship("User", back_populates="tokens")

    @property
    def dict(self):
        return {
            "id": self.id,
        }


class Ads(Base):
    __tablename__ = "aiohttp_ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    owner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("aiohttp_users.id", ondelete="CASCADE")
    )

    owner = relationship("User", back_populates="ads")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": int(self.created_at.timestamp()),
            "owner": self.owner,
            "owner_id": self.owner_id,
        }


async def init_orm():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
