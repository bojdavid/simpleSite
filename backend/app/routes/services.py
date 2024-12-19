from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from .. import schemas
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from typing import List


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


#get all services
@router.get("/", response_model=List[schemas.ServiceOut])
async def getAllServices(db : MongoClient = Depends(get_db)):
    services = list(db["services"].find())
    for service in services:
        service['_id'] = str(service['_id'])  # Convert ObjectId to string for JSON serialization
    return services


#create a service
@router.post("/", response_model=schemas.ServiceOut)
async def createService(data : schemas.ServiceCreate, db: MongoClient = Depends(get_db)):
    try:
        result = db["services"].insert_one(data.model_dump())
        inserted_item = db["services"].find_one({"_id": ObjectId(result.inserted_id)})
        inserted_item['_id'] = str(inserted_item['_id'])
        return inserted_item
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inserting item: {str(e)}")


#get a service
@router.get("/{id}", response_model=schemas.ServiceOut)
async def getService(id: str, db : MongoClient = Depends(get_db)):
    service = db["services"].find_one({"_id" : ObjectId(id)})

    if service == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    
    # Convert ObjectId to string for JSON serialization
    service['_id'] = str(service['_id'])
    return service