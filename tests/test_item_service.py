import pytest
from unittest.mock import MagicMock, patch

with patch("employee.infrastructure.item_repository.Base.metadata.create_all"):
    from employee.application.item_service import ItemService
from employee.domain.generated_models.models import Items as DBItem

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def service(mock_repo):
    with patch("employee.application.item_service.ItemRepositoryImpl", return_value=mock_repo):
        yield ItemService()

def test_get_item_found(service, mock_repo):
    mock_repo.get_by_id.return_value = DBItem(id=1, name="item1", description="desc")
    from employee.application.item_schemas import ItemResponse
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
    from employee.application.item_schemas import ItemResponse
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
    from employee.application.item_schemas import ItemUpdateRequest, ItemResponse
    req = ItemUpdateRequest(name="updated", description="desc")
    result = service.update_item(1, req)
    assert isinstance(result, ItemResponse)
    assert result.name == "updated"

def test_update_item_not_found(service, mock_repo):
    mock_repo.update.return_value = None
    from employee.application.item_schemas import ItemUpdateRequest
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
    from employee.application.item_schemas import ItemUpdateRequest
    req = ItemUpdateRequest(name="valid", description="desc")
    assert req.name == "valid"
    assert req.description == "desc"

import pytest

def test_item_update_request_validation_empty_name():
    from employee.application.item_schemas import ItemUpdateRequest
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="", description="desc")

def test_item_update_request_validation_long_description():
    from employee.application.item_schemas import ItemUpdateRequest
    long_desc = "a" * 256
    with pytest.raises(ValueError):
        ItemUpdateRequest(name="valid", description=long_desc)
