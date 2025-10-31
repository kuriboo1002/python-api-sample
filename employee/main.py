import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Body
from employee.application.item_service import ItemService
from employee.application.item_schemas import ItemUpdateRequest, ItemResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
item_service = ItemService()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items", response_model=list[ItemResponse])
def read_items():
    items = item_service.get_items()
    return items

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, req: ItemUpdateRequest):
    item = item_service.update_item(item_id, req)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    result = item_service.delete_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "success"}
