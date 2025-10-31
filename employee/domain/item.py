from abc import ABC, abstractmethod
from typing import Optional
from employee.infrastructure.generated_models.models import Items as DBItem

from employee.domain.value_objects import Name, Description

class Item:
    def __init__(self, name: str, description: str):
        self.name = Name(name)
        self.description = Description(description)

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[DBItem]:
        pass

    @abstractmethod
    def get_all(self) -> list[DBItem]:
        pass

    @abstractmethod
    def update(self, item_id: int, req) -> Optional[DBItem]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
