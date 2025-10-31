import pytest
from unittest.mock import MagicMock
from employee.application.item_service import ItemService
from employee.application.item_schemas import ItemUpdateRequest, ItemResponse, ItemCreateRequest
from employee.infrastructure.generated_models.models import Items as DBItem

# サービス層（ユースケース）テスト
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return ItemService(mock_repo)

def test_service_get_item_found(service, mock_repo):
    mock_repo.get_by_id.return_value = DBItem(id=1, name="item1", description="desc")
    result = service.get_item(1)
    assert isinstance(result, ItemResponse)
    assert result.id == 1

def test_service_get_item_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = service.get_item(999)
    assert result is None

def test_service_get_items_returns_list(service, mock_repo):
    mock_repo.get_all.return_value = [
        DBItem(id=1, name="item1", description="desc"),
        DBItem(id=2, name="item2", description="desc2"),
    ]
    result = service.get_items()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, ItemResponse) for item in result)

def test_service_get_items_empty(service, mock_repo):
    mock_repo.get_all.return_value = []
    result = service.get_items()
    assert result == []

def test_service_update_item_success(service, mock_repo):
    mock_repo.update.return_value = DBItem(id=1, name="updated", description="desc")
    req = ItemUpdateRequest(name="updated", description="desc")
    result = service.update_item(1, req)
    assert isinstance(result, ItemResponse)
    assert result.name == "updated"

def test_service_update_item_not_found(service, mock_repo):
    mock_repo.update.return_value = None
    req = ItemUpdateRequest(name="updated", description="desc")
    result = service.update_item(999, req)
    assert result is None

def test_service_delete_item_success(service, mock_repo):
    mock_repo.delete.return_value = True
    result = service.delete_item(1)
    assert result is True

def test_service_delete_item_not_found(service, mock_repo):
    mock_repo.delete.return_value = False
    result = service.delete_item(999)
    assert result is False

def test_service_create_item_success(service, mock_repo):
    mock_repo.get_all.return_value = []
    mock_repo.create.return_value = DBItem(id=1, name="newitem", description="desc")
    req = ItemCreateRequest(name="newitem", description="desc")
    result = service.create_item(req)
    assert isinstance(result, ItemResponse)
    assert result.name == "newitem"

def test_service_create_item_duplicate_name(service, mock_repo):
    mock_repo.get_all.return_value = [DBItem(id=1, name="newitem", description="desc")]
    req = ItemCreateRequest(name="newitem", description="desc")
    with pytest.raises(ValueError):
        service.create_item(req)
