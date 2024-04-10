from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from ..core.config import settings, Logger
from typing import Annotated

log = Logger(__name__, 'base.log').logger

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]