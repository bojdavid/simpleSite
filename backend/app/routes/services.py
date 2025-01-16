from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from .. import schemas, ouath2
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from typing import List, Annotated


router = APIRouter(
    prefix="/api/v1/services",
    tags=["Services"]
)


# GET ALL SERVICES
@router.get("/", response_model=List[schemas.ServiceOut])
async def getAllServices(db : MongoClient = Depends(get_db)):
    services = list(db["services"].find())
    for service in services:
        service['_id'] = str(service['_id'])  # Convert ObjectId to string for JSON serialization
    return services


# ADD A SERVICE
@router.post("/", response_model=schemas.ServiceOut, status_code=status.HTTP_201_CREATED)
async def createService(data : schemas.ServiceCreate, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], db: MongoClient = Depends(get_db)):
    try:
        result = db["services"].insert_one(data.model_dump())
        inserted_item = db["services"].find_one({"_id": ObjectId(result.inserted_id)})
        inserted_item['_id'] = str(inserted_item['_id'])
        return inserted_item
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inserting item: {str(e)}")


# GET A SINGLE SERVICE
@router.get("/{id}", response_model=schemas.ServiceOut)
async def getService(id: str, db : MongoClient = Depends(get_db)):
    service = db["services"].find_one({"_id" : ObjectId(id)})

    if service == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    
    # Convert ObjectId to string for JSON serialization
    service['_id'] = str(service['_id'])
    return service


# UPDATE A SERVICE
@router.put("/{id}", response_model=schemas.ServiceOut)
async def updateService(data: schemas.ServiceUpdate, id : str, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], db : MongoClient = Depends(get_db)):
    service = db["services"].find_one({"_id" : ObjectId(id)})

    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service with id of {id} was not found")

     # Prepare the update data
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    # Update the service in the database
    db["services"].update_one({"_id": ObjectId(id)}, {"$set": update_data})

    # Retrieve the updated service
    updated_service = db["services"].find_one({"_id": ObjectId(id)})
    updated_service['_id'] = str(updated_service['_id'])  # Convert ObjectId to string for JSON serialization

    return schemas.ServiceOut(**updated_service)  # Return the updated service



# DELETE A SERVICE
@router.delete("/{id}")
async def getService(id: str, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], db : MongoClient = Depends(get_db)):
    result = db["services"].delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    
    return  {"Message": f"Service with id of {id} has been deleted successfully"}


# APPROVE A SERVICE
@router.put("/approve/{id}")
async def approveService(id: str, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], data : schemas.ServiceApprove, db : MongoClient = Depends(get_db)):
    service = db["services"].find_one({"_id" : ObjectId(id)})
    
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"service with id of {id} was not found")
    db["services"].update_one({"_id": ObjectId(id)}, {"$set": data.model_dump()})
    if data.isApproved:
        return {"Message": f"service with id of {id} has been approved successfully"}
    else:
        return {"Message": f"service with id of {id} has been disapproved successfully"}
 