from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    def __init__(self, entity_type: Type[T]):
        self.type = entity_type

    @abstractmethod
    def get(self, unique_index: Any) -> T:
        pass

    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def update(self, data: T) -> T:
        pass

    @abstractmethod
    def delete(self, unique_index: Any) -> None:
        pass

