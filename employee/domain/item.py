from __future__ import annotations
from typing import Optional

from abc import ABC, abstractmethod

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[CustomItem]:
        pass

    @abstractmethod
    def get_all(self) -> list[CustomItem]:
        pass

    @abstractmethod
    def update(self, item_id: int, name: str, description: str) -> Optional[CustomItem]:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> bool:
        pass

from employee.domain.generated_models.models import Items as BaseItem

class CustomItem(BaseItem):
    # 追加メソッドやプロパティをここに記述
    pass
