import pytest
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from src.dependencies import (
    get_db,
    get_item_repository,
    get_command_service,
    get_query_service,
)
from src.infrastructure.item_repository import ItemRepositoryImpl
from src.infrastructure.item_repository_adapter import ItemRepositoryAdapter
from src.application.item_command_service import ItemCommandService
from src.application.item_query_service import ItemQueryService
from src.domain.item import ItemRepository


def test_get_db():
    """
    Test the get_db dependency generator.
    It should yield a database session and then close it.
    """
    with patch("src.dependencies.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db

        db_generator = get_db()
        db_session = next(db_generator)

        # Check if the yielded value is the mock session
        assert db_session == mock_db

        # Check if the session is closed upon generator exit
        with pytest.raises(StopIteration):
            next(db_generator)

        mock_db.close.assert_called_once()


def test_get_item_repository():
    """
    Test the get_item_repository dependency.
    It should return an instance of ItemRepositoryImpl.
    """
    mock_db_session = MagicMock(spec=Session)
    repo = get_item_repository(db=mock_db_session)
    assert isinstance(repo, ItemRepositoryImpl)
    assert isinstance(repo.adapter, ItemRepositoryAdapter)


def test_get_command_service():
    """
    Test the get_command_service dependency.
    It should return an instance of ItemCommandService.
    """
    mock_repo = MagicMock(spec=ItemRepository)
    service = get_command_service(repo=mock_repo)
    assert isinstance(service, ItemCommandService)


def test_get_query_service():
    """
    Test the get_query_service dependency.
    It should return an instance of ItemQueryService.
    """
    mock_repo = MagicMock(spec=ItemRepository)
    service = get_query_service(repo=mock_repo)
    assert isinstance(service, ItemQueryService)
