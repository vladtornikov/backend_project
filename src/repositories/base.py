import logging

from fastapi import HTTPException
from typing import Any

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError


from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model =  None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list[BaseModel | None]:
        return await self.get_filtered()

    async def get_filtered(self, *filter: Any, **filter_by: Any) -> list[BaseModel]:
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        data = result.scalars().all()
        return [self.mapper.map_to_domain_entity(model) for model in data]


    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | None:
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(add_data_stmt.compile(compile_kwargs={'literal_binds': True}))
        try:
            result = await self.session.execute(add_data_stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                logging.exception(
                    f'Не удалось добавить данные в БД, входные данные={data}'
                )
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception(
                    f'Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}'
                )
                raise ex
        model = result.scalar_one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]) -> None:
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        print(add_data_stmt.compile(compile_kwargs={'literal_binds':True}))
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        try:
            await self.check_data(filter_by)
        except NoResultFound:
            raise ObjectNotFoundException
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        try:
            await self.session.execute(stmt)
        except IntegrityError or NoResultFound:
            raise ObjectNotFoundException

    async def delete(self, **filter_by) -> None:
        stmt = select(self.model).filter_by(**filter_by)
        obj = await self.session.execute(stmt)
        try:
            obj.scalars().all()
        except NoResultFound:
            raise ObjectNotFoundException
        stmt = delete(self.model).filter_by(**filter_by)
        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)

    async def check_data(self, filter_by: dict):
        stmt = select(self.model).filter_by(**filter_by)
        obj = await self.session.execute(stmt)
        try:
            res = obj.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
