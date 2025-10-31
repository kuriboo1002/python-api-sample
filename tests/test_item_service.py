import pytest
from unittest.mock import MagicMock
from employee.service.item_service import ItemService
from employee.service.item_schemas import ItemUpdateRequest, ItemResponse, ItemCreateRequest
from employee.domain.generated_models.models import Items as DBItem

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return ItemService(mock_repo)

def test_get_item_found(service, mock_repo):
    mock_repo.get_by_id.return_value = DBItem(id=1, name="item1", description="desc")
    result = service.get_item(1)
    assert isinstance(result, ItemResponse)
    assert result.id == 1

def test_get_item_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    result = service.get_item(999)
    assert result is None

def test_get_items_returns_list(service, mock_repo):
    mock_repo.get_all.return_value = [
        DBItem(id=1, name="item1", description="desc"),
        DBItem(id=2, name="item2", description="desc2"),
    ]
    result = service.get_items()
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(item, ItemResponse) for item in result)

def test_get_items_empty(service, mock_repo):
    mock_repo.get_all.return_value = []
    result = service.get_items()
    assert result == []

def test_update_item_success(service, mock_repo):
    mock_repo.update.return_value = DBItem(id=1, name="updated", description="desc")
    req = ItemUpdateRequest(name="updated", description="desc")
    result = service.update_item(1, req)
    assert isinstance(result, ItemResponse)
    assert result.name == "updated"

def test_update_item_not_found(service, mock_repo):
    mock_repo.update.return_value = None
    req = ItemUpdateRequest(name="updated", description="desc")
    result = service.update_item(999, req)
    assert result is None

def test_delete_item_success(service, mock_repo):
    mock_repo.delete.return_value = True
    result = service.delete_item(1)
    assert result is True

def test_delete_item_not_found(service, mock_repo):
    mock_repo.delete.return_value = False
    result = service.delete_item(999)
    assert result is False

def test_item_update_request_validation_success():
    req = ItemUpdateRequest(name="valid", description="desc")
    assert req.name == "valid"
    assert req.description == "desc"

def test_item_update_request_validation_empty_name():
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="", description="desc")

def test_item_update_request_validation_long_description():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="valid", description=long_desc)

def test_item_create_request_success():
    req = ItemCreateRequest(name="newitem", description="desc")
    assert req.name == "newitem"
    assert req.description == "desc"

def test_item_create_request_empty_name():
    with pytest.raises(ValueError):
        ItemCreateRequest(name="", description="desc")

def test_item_create_request_long_description():
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        ItemCreateRequest(name="valid", description=long_desc)
