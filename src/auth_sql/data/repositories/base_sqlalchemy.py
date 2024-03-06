'''
    SQLAlchemy repository abstraction
'''
from typing import List
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from data.tables.base import BasePublic
from data.repositories.base import RepositoryBase


T = TypeVar("T", bound=BasePublic)


class SQLAlchemyRepository(RepositoryBase):
    '''
        SQLAlchemy repository abstraction
    '''

    model: T = None

    def __init__(self, url: str, echo: bool = False, **kwargs):
        super().__init__(url=url, **kwargs)

        engine = create_async_engine(self.url, echo=echo)
        self.session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=True)

    # SELECT

    async def find(self, join_rels=False, **filter_by) -> List[T]:
        async with self.session_factory() as session:
            query = select(self.model)
            if join_rels:
                query = query.options(joinedload('*'))
            query = query.filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalars().all()

    async def find_one_or_none(self, join_rels=False, **filter_by) -> T | None:
        async with self.session_factory() as session:
            query = select(self.model)
            if join_rels:
                query = query.options(joinedload('*'))
            query = query.filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalars().one_or_none()

    # INSERT

    async def add_one(self, data: BaseModel) -> dict:
        async with self.session_factory() as session:
            query = insert(self.model).values(**data.model_dump()).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()

            return result.mappings().first()

    async def add_many(self, datas: List[BaseModel]) -> dict:
        async with self.session_factory() as session:
            datas = [data.model_dump() for data in datas]
            query = insert(self.model).values(datas).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()

            return result.mappings().first()

    # UPDATE

    async def edit_one(self, id: int, data: dict) -> int:
        async with self.session_factory() as session:
            query = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            result = await session.execute(query)
            await session.commit()

            return result.mappings().first()

    # DELETE

    async def delete_one(self, **filter_by):
        async with self.session_factory() as session:
            query = delete(self.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
