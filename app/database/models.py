from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config_reader import config 
DB_URL=config.DB_URL.get_secret_value()

engine = create_async_engine(url=DB_URL,
                             echo=False) # Set True if you want see all logs
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username = mapped_column(String(32))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)