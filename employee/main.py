from fastapi import FastAPI
from employee.api.item_api import router

app = FastAPI()
app.include_router(router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}
