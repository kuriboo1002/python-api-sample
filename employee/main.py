import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Body
from employee.application.item_service import ItemService
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
item_service = ItemService()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "description": item.description}

@app.get("/items")
def read_items():
    items = item_service.get_items()
    return JSONResponse(
        content=[
            {"id": i.id, "name": i.name, "description": i.description}
            for i in items
        ],
        media_type="application/json; charset=utf-8"
    )

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str = Body(...), description: str = Body(...)):
    item = item_service.update_item(item_id, name, description)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item.id, "name": item.name, "description": item.description}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    result = item_service.delete_item(item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"result": "success"}
