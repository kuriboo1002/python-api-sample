from typing import Optional

from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(TEXT)
