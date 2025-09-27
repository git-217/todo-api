from typing import Annotated
from sqlalchemy.orm import mapped_column

str_unique = Annotated[str, mapped_column(unique=True, nullable=False)]
