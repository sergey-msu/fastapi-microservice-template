from datetime import datetime as dt

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime
from sqlalchemy import String

from data.tables.base import BasePublic


class Token(BasePublic):
    __tablename__ = 'tokens'

    create_date: Mapped[dt] = mapped_column(DateTime, nullable=False)
    access_token: Mapped[str] = mapped_column(String[1024], nullable=False)
    refresh_token: Mapped[str] = mapped_column(String[1024], nullable=False)
    token_type: Mapped[str] = mapped_column(String[32], nullable=False)
