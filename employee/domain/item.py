from abc import ABC, abstractmethod
from typing import Optional
from employee.domain.generated_models.models import Items as DBItem

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
