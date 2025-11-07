from abc import ABC, abstractmethod
from typing import Optional

from employee.domain.value_objects import Name, Description

class Item:
    def __init__(self, name: str, description: str, id: int = None, **kwargs):
        self.id = id
        self.name = Name(name)
        self.description = Description(description)
        # 追加項目も自動セット
        for k, v in kwargs.items():
            if not hasattr(self, k):
                setattr(self, k, v)

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[Item]:
        pass

    @abstractmethod
    def get_all(self) -> list[Item]:
        pass

    @abstractmethod
    def update(self, item_id: int, req) -> Optional[Item]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass
