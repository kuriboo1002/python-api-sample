import pytest
from unittest.mock import MagicMock
from src.domain.item import Item
from src.infrastructure.item_repository import ItemRepositoryImpl, dbitem_to_item
from src.infrastructure.item_repository_adapter import ItemRepositoryAdapter
from src.infrastructure.generated_models.models import Items as DBItem

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def item_repository_adapter(mock_db_session):
    return ItemRepositoryAdapter(db=mock_db_session)

@pytest.fixture
def item_repository(item_repository_adapter):
    return ItemRepositoryImpl(adapter=item_repository_adapter)

def test_dbitem_to_item():
    db_item = DBItem(id=1, name="Test Item", description="Test Description")
    item = dbitem_to_item(db_item)
    assert item.id == 1
    assert item.name.value == "Test Item"
    assert item.description.value == "Test Description"

def test_dbitem_to_item_none():
    assert dbitem_to_item(None) is None

def test_get_by_id(item_repository, item_repository_adapter):
    db_item = DBItem(id=1, name="Test Item", description="Test Description")
    item_repository_adapter.get_by_id = MagicMock(return_value=db_item)
    
    item = item_repository.get_by_id(1)
    
    assert item.id == 1
    item_repository_adapter.get_by_id.assert_called_once_with(1)

def test_get_all(item_repository, item_repository_adapter):
    db_items = [DBItem(id=1, name="Test Item 1", description="Test Description 1")]
    item_repository_adapter.get_all = MagicMock(return_value=db_items)
    
    items = item_repository.get_all()
    
    assert len(items) == 1
    assert items[0].id == 1
    item_repository_adapter.get_all.assert_called_once()

def test_create(item_repository, item_repository_adapter):
    req = Item(name="New Item", description="New Description")
    db_item = DBItem(id=1, name="New Item", description="New Description")
    item_repository_adapter.create = MagicMock(return_value=db_item)
    
    item = item_repository.create(req)
    
    assert item.id == 1
    item_repository_adapter.create.assert_called_once_with(req)

def test_update(item_repository, item_repository_adapter):
    req = Item(name="Updated Item", description="Updated Description")
    db_item = DBItem(id=1, name="Updated Item", description="Updated Description")
    item_repository_adapter.update = MagicMock(return_value=db_item)
    
    item = item_repository.update(1, req)
    
    assert item.id == 1
    item_repository_adapter.update.assert_called_once_with(1, req)

def test_delete(item_repository, item_repository_adapter):
    item_repository_adapter.delete = MagicMock(return_value=True)
    
    result = item_repository.delete(1)
    
    assert result is True
    item_repository_adapter.delete.assert_called_once_with(1)

def test_adapter_get_by_id(item_repository_adapter, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = DBItem()
    item_repository_adapter.get_by_id(1)
    mock_db_session.query.assert_called_once_with(DBItem)

def test_adapter_get_all(item_repository_adapter, mock_db_session):
    mock_db_session.query.return_value.all.return_value = []
    item_repository_adapter.get_all()
    mock_db_session.query.assert_called_once_with(DBItem)

def test_adapter_create(item_repository_adapter, mock_db_session):
    req = Item(name="New Item", description="New Description")
    item_repository_adapter.create(req)
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_adapter_update(item_repository_adapter, mock_db_session):
    req = Item(name="Updated Item", description="Updated Description")
    mock_db_session.query.return_value.filter.return_value.first.return_value = DBItem()
    item_repository_adapter.update(1, req)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_adapter_update_not_found(item_repository_adapter, mock_db_session):
    req = Item(name="Updated Item", description="Updated Description")
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    result = item_repository_adapter.update(1, req)
    assert result is None

def test_adapter_delete(item_repository_adapter, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = DBItem()
    item_repository_adapter.delete(1)
    mock_db_session.delete.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_adapter_delete_not_found(item_repository_adapter, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    result = item_repository_adapter.delete(1)
    assert result is False
