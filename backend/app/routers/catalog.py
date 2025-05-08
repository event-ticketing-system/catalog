from typing import List
from fastapi import APIRouter,  HTTPException, UploadFile, File
from bson.objectid import ObjectId
from ..serializers.catalogSerializers import eventEntity, orderRequest
import os
import shutil

from app.database import Catalog, Orders
from ..schemas import *

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  

@router.get("/events", response_model=List[EventBaseModel])
def list_events():
    return [eventEntity(e) for e in Catalog.find()]

@router.get("/events/{event_id}", response_model=EventBaseModel)
def get_event(event_id: str):
    e = Catalog.find_one({"_id": ObjectId(event_id)})
    if not e:
        raise HTTPException(status_code=404, detail="Event not found")
    return eventEntity(e)

@router.post("/upload-image/")
def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"url": f"/uploads/{file.filename}"}

@router.post("/events", response_model=EventBaseModel)  # New POST route
def create_event(event: EventBaseModel):
    # Prepare event data
    event_data = event.dict()

    # Set the created_at and updated_at fields to current UTC time
    event_data['created_at'] = event_data['updated_at'] = datetime.utcnow()

    # Insert event into database
    result = Catalog.insert_one(event_data)

    # Get the inserted event and return the response
    new_event = Catalog.find_one({"_id": result.inserted_id})

    if not new_event:
        raise HTTPException(status_code=500, detail="Failed to create event")

    return eventEntity(new_event)

@router.post("/orders")
def create_order(order: OrderSchema):
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    total_price = order.quantity * order.price
    order_data = {
        "event_id": order.event_id,
        "event_name": order.event_name,
        "quantity": order.quantity,
        "price": order.price,
        "total_price": total_price,
        "order_time": datetime.utcnow(),
    }

    result = Orders.insert_one(order_data)
    new_order = Orders.find_one({"_id": result.inserted_id})

    return orderRequest(new_order)