import asyncio
import datetime

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncAttrs, AsyncSession)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

# DATABESE_URL = "{type_bd}+{engine}://{user}:{passw}@{host}:{port}/{db}"


DATABESE_URL = "sqlite+aiosqlite:///./test.db"
# DATABESE_URL = "postgresql+asyncpg://scott:tiger@localhost:5432/test"
# DATABESE_URL = "mysql+aiomysql://scott:tiger@localhost/test"


engine = create_async_engine(DATABESE_URL, echo=True)
async_session = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    age: Mapped[int]


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        sess.add(User(name="admin", age=18))
        sess.add(User(name="user", age=28))
        await sess.commit()


async def main():
    await create_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
