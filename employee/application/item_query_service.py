from employee.application.item_schemas import ItemResponse

class ItemQueryService:
    def __init__(self, repo):
        self.repo = repo

    def get_item(self, item_id: int) -> ItemResponse:
        item = self.repo.get_by_id(item_id)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def get_items(self) -> list[ItemResponse]:
        items = self.repo.get_all()
        return [ItemResponse(id=i.id, name=i.name, description=i.description) for i in items]
