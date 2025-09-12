from typing import TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import (select,
                        update as sqlalchemy_update, 
                        delete as sqlalchemy_delete)
from backend.app.db.base import BaseSAModel

ModelType = TypeVar('ModelType', bound=BaseSAModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Default CRUD object with create/read/update/delete methods
    """
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get(self, *, db: AsyncSession, id: int) -> ModelType | None:
        return await db.get(self.model, id)
    
    async def get_list(self, db: AsyncSession,) -> list[ModelType] | None:
        result = await db.execute(select(self.model))
        return result.scalars().all()
    
    async def create(self,
                     *,
                     db: AsyncSession,
                     obj_data: CreateSchemaType | ModelType,
                    ) -> ModelType:
        try:
            new_obj = self.model(**obj_data)
            db.add(new_obj)
            print(obj_data)
            await db.flush()
            return new_obj
        except Exception as e:
            raise e
        
    async def update(self, *, db: AsyncSession, filter_by, **values: dict) -> int:
        new_obj = (
            sqlalchemy_update(self.model)
            .where(*[getattr(self.model, k) == v for k,v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session='fetch')
        )
        result = await db.execute(new_obj)
        return result.rowcount
    
    async def delete(self, *, db: AsyncSession, **filter_by) -> int:
        new_obj = (
            sqlalchemy_delete(self.model)
            .filter_by(**filter_by)
        )
        result = await db.execute(new_obj)
        return result.rowcount        