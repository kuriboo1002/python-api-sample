from employee.domain.item import ItemRepository
from employee.infrastructure.generated_models.models import Items as DBItem

class ItemRepositoryImpl(ItemRepository):
    def __init__(self, adapter):
        self.adapter = adapter

    def get_by_id(self, item_id: int) -> DBItem | None:
        return self.adapter.get_by_id(item_id)

    def get_all(self) -> list[DBItem]:
        return self.adapter.get_all()

    def update(self, item_id: int, req) -> DBItem | None:
        return self.adapter.update(item_id, req)

    def delete(self, item_id: int) -> bool:
        return self.adapter.delete(item_id)

    def create(self, req) -> DBItem:
        return self.adapter.create(req)
