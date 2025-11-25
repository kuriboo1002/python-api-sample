from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.item_command_service import ItemCommandService
from src.application.item_query_service import ItemQueryService
from src.domain.item import ItemRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.item_repository import ItemRepositoryImpl
from src.infrastructure.item_repository_adapter import ItemRepositoryAdapter


# Dependency for database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency for ItemRepository
def get_item_repository(db: Session = Depends(get_db)) -> ItemRepository:
    adapter = ItemRepositoryAdapter(db)
    return ItemRepositoryImpl(adapter)


# Dependency for ItemCommandService
def get_command_service(
    repo: ItemRepository = Depends(get_item_repository),
) -> ItemCommandService:
    return ItemCommandService(repo)


# Dependency for ItemQueryService
def get_query_service(
    repo: ItemRepository = Depends(get_item_repository),
) -> ItemQueryService:
    return ItemQueryService(repo)
