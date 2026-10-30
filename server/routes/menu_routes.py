from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from server.config.database import get_db
from server.models import schemas
from server.controllers import menu_controller

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.post("", response_model=schemas.MenuItemResponse)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return menu_controller.create_menu_item(item, db)

@router.get("", response_model=List[schemas.MenuItemResponse])
def get_menu_items(category: Optional[str] = None, db: Session = Depends(get_db)):
    return menu_controller.get_menu_items(category, db)

@router.get("/{item_id}", response_model=schemas.MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    return menu_controller.get_menu_item(item_id, db)

@router.put("/{item_id}", response_model=schemas.MenuItemResponse)
def update_menu_item(item_id: int, item_update: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    return menu_controller.update_menu_item(item_id, item_update, db)

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    return menu_controller.delete_menu_item(item_id, db)

@router.post("/{item_id}/image", response_model=schemas.MenuItemResponse)
async def upload_menu_item_image(item_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await menu_controller.upload_menu_item_image(item_id, file, db)
