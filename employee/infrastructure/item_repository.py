import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from employee.domain.item import ItemRepository
from employee.domain.generated_models.models import Items as DBItem

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "employee_db")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, connect_args={"use_unicode": True})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ItemModelは自動生成モデル(DBItem)に置き換え
Base.metadata.create_all(bind=engine)

class ItemRepositoryImpl(ItemRepository):
    def get_by_id(self, item_id: int) -> DBItem | None:
        db = SessionLocal()
        item = db.query(DBItem).filter(DBItem.id == item_id).first()
        db.close()
        return item

    def get_all(self) -> list[DBItem]:
        db = SessionLocal()
        items = db.query(DBItem).all()
        db.close()
        return items

    def update(self, item_id: int, req) -> DBItem | None:
        db = SessionLocal()
        item = db.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            db.close()
            return None
        item.name = req.name
        item.description = req.description
        db.commit()
        db.refresh(item)
        db.close()
        return item

    def delete(self, item_id: int) -> bool:
        db = SessionLocal()
        item = db.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            db.close()
            return False
        db.delete(item)
        db.commit()
        db.close()
        return True
