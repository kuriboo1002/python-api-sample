import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from src.main import app
from src.dependencies import get_command_service, get_query_service
from src.application.item_schemas import ItemResponse

# Mock services
mock_command_service = MagicMock()
mock_query_service = MagicMock()


def override_get_command_service():
    return mock_command_service


def override_get_query_service():
    return mock_query_service


app.dependency_overrides[get_command_service] = override_get_command_service
app.dependency_overrides[get_query_service] = override_get_query_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mocks():
    mock_command_service.reset_mock()
    mock_query_service.reset_mock()


def test_create_item():
    # Setup
    mock_command_service.create_item.return_value = ItemResponse(
        id=1, name="Test Item", description="A test item"
    )
    item_data = {"name": "Test Item", "description": "A test item"}

    # Execute
    response = client.post("/items", json=item_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Item",
        "description": "A test item",
    }
    mock_command_service.create_item.assert_called_once()


def test_create_item_value_error():
    # Setup
    mock_command_service.create_item.side_effect = ValueError("Invalid item name")
    item_data = {"name": "Invalid", "description": "A test item"}

    # Execute
    response = client.post("/items", json=item_data)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid item name"}
    mock_command_service.create_item.assert_called_once()



def test_update_item():
    # Setup
    mock_command_service.update_item.return_value = ItemResponse(
        id=1, name="Updated Item", description="An updated item"
    )
    item_data = {"name": "Updated Item", "description": "An updated item"}

    # Execute
    response = client.put("/items/1", json=item_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Updated Item",
        "description": "An updated item",
    }
    mock_command_service.update_item.assert_called_once()


def test_update_item_not_found():
    # Setup
    mock_command_service.update_item.return_value = None
    item_data = {"name": "Updated Item", "description": "An updated item"}

    # Execute
    response = client.put("/items/999", json=item_data)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    mock_command_service.update_item.assert_called_once()


def test_delete_item():
    # Setup
    mock_command_service.delete_item.return_value = True

    # Execute
    response = client.delete("/items/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"result": "success"}
    mock_command_service.delete_item.assert_called_once_with(1)


def test_delete_item_not_found():
    # Setup
    mock_command_service.delete_item.return_value = False

    # Execute
    response = client.delete("/items/999")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    mock_command_service.delete_item.assert_called_once_with(999)


def test_get_item():
    # Setup
    mock_query_service.get_item.return_value = ItemResponse(
        id=1, name="Test Item", description="A test item"
    )

    # Execute
    response = client.get("/items/1")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Item",
        "description": "A test item",
    }
    mock_query_service.get_item.assert_called_once_with(1)


def test_get_item_not_found():
    # Setup
    mock_query_service.get_item.return_value = None

    # Execute
    response = client.get("/items/999")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    mock_query_service.get_item.assert_called_once_with(999)


def test_get_items():
    # Setup
    mock_query_service.get_items.return_value = [
        ItemResponse(id=1, name="Item 1", description="First item"),
        ItemResponse(id=2, name="Item 2", description="Second item"),
    ]

    # Execute
    response = client.get("/items")

    # Assert
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Item 1", "description": "First item"},
        {"id": 2, "name": "Item 2", "description": "Second item"},
    ]
    mock_query_service.get_items.assert_called_once()
