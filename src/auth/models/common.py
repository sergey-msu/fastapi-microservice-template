'''
    Commonly used models
'''
from models.base import AppBaseModel


class Result(AppBaseModel):
    ok: bool = True
    msg: str | None = None
    value: str | None = None


OK = Result(ok=True)
NOK = Result(ok=False)


def ok(result: bool):
    return OK if result else NOK
