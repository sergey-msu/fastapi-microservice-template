from data.repositories.base_sqlalchemy import SQLAlchemyRepository
from data import tables


class TokensRepository(SQLAlchemyRepository):
    model = tables.Token

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
