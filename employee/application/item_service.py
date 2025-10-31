from typing import Optional
from employee.infrastructure.item_repository import ItemRepositoryImpl

class ItemService:
    def __init__(self):
        self.repo = ItemRepositoryImpl()


    def get_item(self, item_id: int) -> Optional[ItemResponse]:
        item = self.repo.get_by_id(item_id)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def get_items(self) -> list[ItemResponse]:
        items = self.repo.get_all()
        return [ItemResponse(id=i.id, name=i.name, description=i.description) for i in items]

    def update_item(self, item_id: int, req) -> Optional[ItemResponse]:
        item = self.repo.update(item_id, req)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)
