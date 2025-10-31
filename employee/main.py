from fastapi import FastAPI, HTTPException, Depends
from employee.service.item_service import ItemService
from employee.service.item_schemas import ItemUpdateRequest, ItemResponse, ItemCreateRequest
from employee.infrastructure.item_repository import ItemRepositoryImpl
from employee.infrastructure.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db=Depends(get_db)):
    repo = ItemRepositoryImpl(db)
    item_service = ItemService(repo)
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items", response_model=list[ItemResponse])
def read_items(db=Depends(get_db)):
    repo = ItemRepositoryImpl(db)
    item_service = ItemService(repo)
    items = item_service.get_items()
    return items

@app.post("/items", response_model=ItemResponse)
def create_item(req: ItemCreateRequest, db=Depends(get_db)):
    repo = ItemRepositoryImpl(db)
    item_service = ItemService(repo)
    item = item_service.create_item(req)
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, req: ItemUpdateRequest, db=Depends(get_db)):
    repo = ItemRepositoryImpl(db)
    item_service = ItemService(repo)
    item = item_service.update_item(item_id, req)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db=Depends(get_db)):
    repo = ItemRepositoryImpl(db)
    item_service = ItemService(repo)
    result = item_service.delete_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "success"}
