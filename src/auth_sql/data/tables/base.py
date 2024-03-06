from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class BasePublic(DeclarativeBase):
    metadata = MetaData(schema='public')

    id: Mapped[int] = mapped_column(primary_key=True)
