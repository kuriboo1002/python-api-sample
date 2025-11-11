import pytest
from unittest.mock import MagicMock
from src.application.item_command_service import ItemCommandService
from src.application.item_query_service import ItemQueryService
from src.application.item_schemas import ItemUpdateRequest, ItemResponse, ItemCreateRequest
from src.domain.item import Item

# サービス層（ユースケース）テスト
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def command_service(mock_repo):
    return ItemCommandService(mock_repo)

@pytest.fixture
def query_service(mock_repo):
    return ItemQueryService(mock_repo)

def test_query_service_get_item_found(query_service, mock_repo):
    mock_repo.get_by_id.return_value = Item(id=1, name="item1", description="desc")
    result = query_service.get_item(1)
    assert isinstance(result, ItemResponse)
    assert result.id == 1
    assert result.name == "item1"
    assert result.description == "desc"

def test_query_service_get_item_not_found(query_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = query_service.get_item(999)
    assert result is None

def test_query_service_get_items_returns_list(query_service, mock_repo):
    mock_repo.get_all.return_value = [
        Item(id=1, name="item1", description="desc"),
        Item(id=2, name="item2", description="desc2"),
    ]
    result = query_service.get_items()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, ItemResponse) for item in result)
    assert result[0].id == 1
    assert result[0].name == "item1"
    assert result[0].description == "desc"
    assert result[1].id == 2
    assert result[1].name == "item2"
    assert result[1].description == "desc2"

def test_query_service_get_items_empty(query_service, mock_repo):
    mock_repo.get_all.return_value = []
    result = query_service.get_items()
    assert result == []

def test_command_service_update_item_success(command_service, mock_repo):
    mock_repo.update.return_value = Item(id=1, name="updated", description="desc")
    req = ItemUpdateRequest(name="updated", description="desc")
    result = command_service.update_item(1, req)
    assert isinstance(result, ItemResponse)
    assert result.id == 1
    assert result.name == "updated"
    assert result.description == "desc"

def test_command_service_update_item_not_found(command_service, mock_repo):
    mock_repo.update.return_value = None
    req = ItemUpdateRequest(name="updated", description="desc")
    result = command_service.update_item(999, req)
    assert result is None

def test_command_service_delete_item_success(command_service, mock_repo):
    mock_repo.delete.return_value = True
    result = command_service.delete_item(1)
    assert result is True

def test_command_service_delete_item_not_found(command_service, mock_repo):
    mock_repo.delete.return_value = False
    result = command_service.delete_item(999)
    assert result is False

def test_command_service_create_item_success(command_service, mock_repo):
    mock_repo.get_all.return_value = []
    mock_repo.create.return_value = Item(id=1, name="newitem", description="desc")
    req = ItemCreateRequest(name="newitem", description="desc")
    result = command_service.create_item(req)
    assert isinstance(result, ItemResponse)
    assert result.id == 1
    assert result.name == "newitem"
    assert result.description == "desc"

def test_command_service_create_item_duplicate_name(command_service, mock_repo):
    mock_repo.get_all.return_value = [Item(id=1, name="newitem", description="desc")]
    req = ItemCreateRequest(name="newitem", description="desc")
    with pytest.raises(ValueError):
        command_service.create_item(req)
