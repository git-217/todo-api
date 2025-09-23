from sqlalchemy import text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import BaseSAModel
from backend.app.tools.enums import CompleteStatus


class Note(BaseSAModel):
    title: Mapped[str] = mapped_column(String(128))
    content: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    status: Mapped[CompleteStatus] = mapped_column(
                                    default=CompleteStatus.IN_PROGRESS, 
                                    server_default=text("'in progress'"))
    
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))

    # 1:N book:notes
    book: Mapped['Book'] = relationship(
        'Book',
        uselist=False,
        back_populates='notes'
    )
    # 1:N user:notes
    user: Mapped['User'] = relationship(
        'User',
        uselist=False,
        back_populates='notes'
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, note_title={self.title!r})"

    def __repr__(self):
        return str(self)