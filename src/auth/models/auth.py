'''
    Authentication/authorization models
'''
from models.base import AppBaseModel


class Token(AppBaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
