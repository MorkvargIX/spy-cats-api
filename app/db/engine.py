from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///./spy_cats.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)
