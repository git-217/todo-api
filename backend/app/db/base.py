from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


int_primary_key = Annotated[int, mapped_column(primary_key=True)]
str_unique = Annotated[str, mapped_column(unique=True, nullable=False)]
str_nullable_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
    
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), 
                                                 onupdate=datetime.now(timezone.utc))