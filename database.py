import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///banking.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    birth_date: Mapped[datetime.date]
    balance: Mapped[float]


class TransactionTable(Base):
    __tablename__ = "transactions"
    transaction_id:  Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int]
    user_to_id:  Mapped[int]
    amount: Mapped[float]



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)