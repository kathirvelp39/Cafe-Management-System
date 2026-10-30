from sqlalchemy.orm import Session
from server.models import models, schemas
from fastapi import HTTPException
import os
import aiofiles
import uuid

IMAGE_DIR = "static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def create_item(item: schemas.MenuItemCreate, db: Session):
    new_item = models.MenuItem(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_items(category: str, db: Session):
    query = db.query(models.MenuItem)
    if category:
        query = query.filter(models.MenuItem.category == category)
    return query.all()

def get_item(item_id: int, db: Session):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

def update_item(item_id: int, item_update: schemas.MenuItemUpdate, db: Session):
    item = get_item(item_id, db)
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(item_id: int, db: Session):
    item = get_item(item_id, db)
    db.delete(item)
    db.commit()
    return {"message": "Menu item deleted successfully"}

async def upload_image(item_id: int, file, db: Session):
    item = get_item(item_id, db)
    
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(IMAGE_DIR, unique_filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
        
    item.image_url = f"/static/images/{unique_filename}"
    db.commit()
    db.refresh(item)
    return item
