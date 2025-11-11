from abc import ABC, abstractmethod
from typing import Optional

from src.domain.value_objects import Name, Description

class Item:
    def __init__(self, id: int = None, name: str = None, description: str = None, **kwargs):
        self.id = id
        self.name = Name(name) if name is not None else None
        self.description = Description(description) if description is not None else None

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        pass

    @abstractmethod
    def get_all(self) -> list[Item]:
        pass

    @abstractmethod
    def update(self, item_id: int, req: Item) -> Optional[Item]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass

    @abstractmethod
    def create(self, req: Item) -> bool:
        pass
