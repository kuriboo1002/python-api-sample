from typing import Optional
from employee.application.item_schemas import ItemResponse
from employee.domain.item_factory import ItemFactory
from employee.domain.item_domain_service import ItemDomainService

class ItemService:
    def __init__(self, repo):
        self.repo = repo

    def get_item(self, item_id: int) -> Optional[ItemResponse]:
        item = self.repo.get_by_id(item_id)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def get_items(self) -> list[ItemResponse]:
        items = self.repo.get_all()
        return [ItemResponse(id=i.id, name=i.name, description=i.description) for i in items]

    def update_item(self, item_id: int, req) -> Optional[ItemResponse]:
        _ = ItemFactory.create(req.name, req.description)  # バリデーションのみ実行
        item = self.repo.update(item_id, req)
        if item is None:
            return None
        return ItemResponse(id=item.id, name=item.name, description=item.description)

    def delete_item(self, item_id: int) -> bool:
        return self.repo.delete(item_id)

    def create_item(self, req) -> ItemResponse:
        items = self.repo.get_all()
        # ItemFactoryで生成（バリデーション含む）
        if ItemDomainService.is_duplicate_name(req.name, [ItemFactory.create(i.name, i.description)[0] for i in items]):
            raise ValueError("Duplicate item name is not allowed")
        _ = ItemFactory.create(req.name, req.description)
        item = self.repo.create(req)
        return ItemResponse(id=item.id, name=item.name, description=item.description)
