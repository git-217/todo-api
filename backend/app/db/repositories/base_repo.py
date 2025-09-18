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

    async def get_by_any(self, *, db:AsyncSession, **values) -> ModelType | None:
        query = select(self.model).filter_by(**values)
        return await db.execute(query)

    async def get(self, *, db: AsyncSession, id: int) -> ModelType | None:
        return await db.get(self.model, id)
    
    async def get_list(self, db: AsyncSession) -> list[ModelType] | None:
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self,
                     *,
                     db: AsyncSession,
                     obj_data: CreateSchemaType | ModelType,
                    ) -> ModelType:
        
        new_obj = self.model(**obj_data)
        db.add(new_obj)
        await db.flush()
        return new_obj
        
        
    async def update(self, *, db: AsyncSession, 
                     id: int, 
                     new_data_obj: UpdateSchemaType) -> ModelType:
        new_obj = (
            sqlalchemy_update(self.model)
            .where(self.model.id == id)
            .values(new_data_obj.model_dump(exclude_unset=True))
            .execution_options(synchronize_session='fetch')
        )
        result = await db.execute(new_obj)
        return result.rowcount
    
    async def delete(self, *, db: AsyncSession, **filter_by) -> bool:
        query = (
            sqlalchemy_delete(self.model)
            .filter_by(**filter_by)
        )
        result = await db.execute(query)
        return True if result else False