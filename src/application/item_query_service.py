from src.application.item_schemas import ItemResponse

class ItemQueryService:
    def __init__(self, repo):
        self.repo = repo

    def get_item(self, item_id: int) -> ItemResponse:
        item = self.repo.get_by_id(item_id)
        if item is None:
            return None
        return ItemResponse.from_item(item)

    def get_items(self) -> list[ItemResponse]:
        items = self.repo.get_all()
        return [ItemResponse.from_item(i) for i in items]
