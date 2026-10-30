from sqlalchemy.orm import Session
from fastapi import UploadFile
from server.models import schemas
from server.services import menu_service
from typing import Optional

def create_menu_item(item: schemas.MenuItemCreate, db: Session):
    return menu_service.create_item(item, db)

def get_menu_items(category: Optional[str], db: Session):
    return menu_service.get_items(category, db)

def get_menu_item(item_id: int, db: Session):
    return menu_service.get_item(item_id, db)

def update_menu_item(item_id: int, item_update: schemas.MenuItemUpdate, db: Session):
    return menu_service.update_item(item_id, item_update, db)

def delete_menu_item(item_id: int, db: Session):
    return menu_service.delete_item(item_id, db)

async def upload_menu_item_image(item_id: int, file: UploadFile, db: Session):
    return await menu_service.upload_image(item_id, file, db)
