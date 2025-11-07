from employee.application.item_schemas import ItemCreateRequest, ItemUpdateRequest, ItemResponse
from employee.domain.item_domain_service import ItemDomainService
from employee.domain.item import Item

class ItemCommandService:
    def __init__(self, repo):
        self.repo = repo

    def _to_item(self, req):
        return Item(name=req.name, description=req.description)

    def _normalize_item_for_duplicate(self, item):
        name = item.name.value if hasattr(item.name, "value") else item.name
        description = item.description.value if hasattr(item.description, "value") else item.description
        return Item(name=name, description=description)

    def create_item(self, req: ItemCreateRequest) -> ItemResponse:
        items = self.repo.get_all()
        # 登録済みアイテムを取得し、重複チェックを行う
        normalized_items = [self._normalize_item_for_duplicate(i) for i in items]
        if ItemDomainService.is_duplicate_name(req.name, normalized_items):
            raise ValueError("Duplicate item name is not allowed")
        item = self._to_item(req)
        created_item = self.repo.create(item)
        return ItemResponse.from_item(created_item)

    def update_item(self, item_id: int, req: ItemUpdateRequest) -> ItemResponse:
        item = self._to_item(req)
        updated_item = self.repo.update(item_id, item)
        if updated_item is None:
            return None
        return ItemResponse.from_item(updated_item)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)
