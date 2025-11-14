from src.domain.item import ItemRepository, Item
from src.infrastructure.generated_models.models import Items as DBItem


def dbitem_to_item(dbitem: DBItem) -> Item:
    if dbitem is None:
        return None
    return Item(**dbitem.__dict__)


class ItemRepositoryImpl(ItemRepository):
    def __init__(self, adapter):
        self.adapter = adapter

    def get_by_id(self, item_id: int) -> Item | None:
        dbitem = self.adapter.get_by_id(item_id)
        return dbitem_to_item(dbitem)

    def get_all(self) -> list[Item]:
        dbitems = self.adapter.get_all()
        return [dbitem_to_item(dbitem) for dbitem in dbitems]

    def update(self, item_id: int, req: Item) -> Item | None:
        dbitem = self.adapter.update(item_id, req)
        return dbitem_to_item(dbitem)

    def delete(self, item_id: int) -> bool:
        return self.adapter.delete(item_id)

    def create(self, req: Item) -> Item:
        dbitem = self.adapter.create(req)
        return dbitem_to_item(dbitem)
