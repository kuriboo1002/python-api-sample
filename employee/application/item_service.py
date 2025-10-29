from employee.infrastructure.item_repository import ItemRepositoryImpl
from employee.domain.item import CustomItem

class ItemService:
    def __init__(self):
        self.repo = ItemRepositoryImpl()

    def get_item(self, item_id: int) -> CustomItem | None:
        return self.repo.get_by_id(item_id)

    def get_items(self) -> list[CustomItem]:
        return self.repo.get_all()

    def update_item(self, item_id: int, name: str, description: str) -> CustomItem | None:
        return self.repo.update(item_id, name, description)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)
