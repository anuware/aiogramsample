from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config_reader import config

engine = create_async_engine(config.DB_URL.get_secret_value())
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

session = None

async def init_db():
    global session
    session = async_session()