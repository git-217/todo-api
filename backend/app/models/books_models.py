from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.tools.enums import CompleteStatus
from backend.app.db.base import Base


class Book(Base):
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)
    status: Mapped[CompleteStatus] = mapped_column(
        default=CompleteStatus.IN_PROGRESS, 
        server_default=text("'IN_PROGRESS'")
        )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    
    user: Mapped["User"] = relationship(
        'User',
        uselist=False,
        back_populates='books'
    )

    notes: Mapped[list['Note']] = relationship(
        'Note',
        back_populates='book',
        cascade = "all, delete-orphan"
        )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, book_title={self.title!r})"

    def __repr__(self):
        return str(self)