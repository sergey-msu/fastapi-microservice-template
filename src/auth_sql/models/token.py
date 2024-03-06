'''
    Authentication/authorization models
'''
from datetime import datetime as dt

from pydantic import Field
from models.base import AppBaseModel


class TokenCreating(AppBaseModel):
    access_token: str = Field(max_length=1024)
    refresh_token: str = Field(max_length=1024)
    create_date: dt = Field(default_factory=dt.utcnow)
    token_type: str = 'bearer'


class TokenCreated(TokenCreating):
    id: int
