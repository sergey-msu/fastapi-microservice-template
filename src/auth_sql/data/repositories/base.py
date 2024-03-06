
from typing import Any
from typing import List
from abc import ABC
from abc import abstractmethod

from utils.logging import LogMixin


class RepositoryBase(ABC, LogMixin):
    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    @abstractmethod
    async def find(self, join_rels=False, **filter_by) -> List[Any]:
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(self, join_rels=False, **filter_by) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, data: dict) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, **filter_by):
        raise NotImplementedError
