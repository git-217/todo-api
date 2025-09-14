from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import BaseSAModel
from backend.app.tools.annotations import str_unique
from backend.app.tools.enums import UserRoles


class User(BaseSAModel):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=False)
    email: Mapped[str_unique]
    password_hash: Mapped[str]

    role: Mapped[UserRoles] = mapped_column(default=UserRoles.BASE, server_default=text('"basic_role"'))

    books: Mapped[list['Book']] = relationship(
        "Book",
        back_populates='user',
        cascade='all, delete-orphan'
        )

    notes: Mapped[list['Note']] = relationship(
        "Note",
        back_populates='user',
        cascade='all, delete-orphan'
        )
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_email={self.email!r})"

    def __repr__(self):
        return str(self)