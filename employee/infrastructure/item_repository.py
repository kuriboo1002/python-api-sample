from employee.domain.item import ItemRepository
from employee.domain.generated_models.models import Items as DBItem

class ItemRepositoryImpl(ItemRepository):
    def __init__(self, db):
        self.db = db

    def get_by_id(self, item_id: int) -> DBItem | None:
        return self.db.query(DBItem).filter(DBItem.id == item_id).first()

    def get_all(self) -> list[DBItem]:
        return self.db.query(DBItem).all()

    def update(self, item_id: int, req) -> DBItem | None:
        item = self.db.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            return None
        item.name = req.name
        item.description = req.description
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        item = self.db.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            return False
        self.db.delete(item)
        self.db.commit()
        return True

    def create(self, req) -> DBItem:
        item = DBItem(name=req.name, description=req.description)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
