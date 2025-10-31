from fastapi import APIRouter, Depends, HTTPException
from employee.application.item_command_service import ItemCommandService
from employee.application.item_query_service import ItemQueryService
from employee.application.item_schemas import ItemCreateRequest, ItemUpdateRequest, ItemResponse

from employee.infrastructure.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_command_service(db=Depends(get_db)):
    from employee.infrastructure.item_repository_adapter import ItemRepositoryAdapter
    from employee.infrastructure.item_repository import ItemRepositoryImpl
    adapter = ItemRepositoryAdapter(db)
    repo = ItemRepositoryImpl(adapter)
    return ItemCommandService(repo)

def get_query_service(db=Depends(get_db)):
    from employee.infrastructure.item_repository_adapter import ItemRepositoryAdapter
    from employee.infrastructure.item_repository import ItemRepositoryImpl
    adapter = ItemRepositoryAdapter(db)
    repo = ItemRepositoryImpl(adapter)
    return ItemQueryService(repo)

@router.post("/items", response_model=ItemResponse)
def create_item(req: ItemCreateRequest, service: ItemCommandService = Depends(get_command_service)):
    try:
        return service.create_item(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, req: ItemUpdateRequest, service: ItemCommandService = Depends(get_command_service)):
    result = service.update_item(item_id, req)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@router.delete("/items/{item_id}")
def delete_item(item_id: int, service: ItemCommandService = Depends(get_command_service)):
    result = service.delete_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "success"}

@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, service: ItemQueryService = Depends(get_query_service)):
    result = service.get_item(item_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result

@router.get("/items", response_model=list[ItemResponse])
def get_items(service: ItemQueryService = Depends(get_query_service)):
    return service.get_items()
