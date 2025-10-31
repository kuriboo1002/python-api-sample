from employee.application.item_schemas import ItemCreateRequest, ItemUpdateRequest, ItemResponse

class ItemCommandService:
    def __init__(self, repo):
        self.repo = repo

    def create_item(self, req: ItemCreateRequest) -> ItemResponse:
        item = self.repo.create(req)
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def update_item(self, item_id: int, req: ItemUpdateRequest) -> ItemResponse:
        item = self.repo.update(item_id, req)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)
