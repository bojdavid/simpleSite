from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, ouath2
from ..database import get_db
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from typing import Annotated

router = APIRouter(
    prefix="/api/v1/bio",
    tags=["Bio"]
)

# GET BIO
@router.get("/{id}", response_model=schemas.BioOut)
async def getBio(id : str, db: MongoClient = Depends(get_db)):
    bio = db["bio"].find_one({"_id" : ObjectId(id)})

    if bio == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bio not found")

    # Convert ObjectId to string for JSON serialization
    bio['_id'] = str(bio['_id'])
    return bio


# CREATE BIO
@router.post("/", response_model=schemas.BioOut)
async def createBio(data: schemas.Bio, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], db: MongoClient = Depends(get_db)):
    """
        User can only post data the first time they are creating their own bio.
    """
    try:
        result = db["bio"].insert_one(data.model_dump())
        inserted_item = db["bio"].find_one({"_id": ObjectId(result.inserted_id)})
        inserted_item['_id'] = str(inserted_item['_id'])
        return inserted_item
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inserting item: {str(e)}")



# UPDATE BIO
@router.put("/{id}")
async def updateBio(id: str, data: schemas.Bio, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], db: MongoClient = Depends(get_db)):
    bio = db["bio"].find_one({"_id": ObjectId(id)})

    if bio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bio with id of {id} was not found")

    # Prepare the update data
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    # Update the bio in the database
    db["bio"].update_one({"_id": ObjectId(id)}, {"$set": update_data})

    # Retrieve the updated bio
    updated_bio = db["bio"].find_one({"_id": ObjectId(id)})
    updated_bio['_id'] = str(updated_bio['_id'])  # Convert ObjectId to string for JSON serialization

    return schemas.BioOut(**updated_bio)