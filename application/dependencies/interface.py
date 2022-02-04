from abc import ABC, abstractmethod


class RPCMethod(ABC):
    @property
    @abstractmethod
    def methods(self) -> list:
        ...


class AsyncInitialization(ABC):
    @classmethod
    @abstractmethod
    async def create(cls):
        ...
