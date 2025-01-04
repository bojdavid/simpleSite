from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Body
from ..database import get_db
from .. import schemas, ouath2
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from typing import List, Annotated

router = APIRouter(
    prefix="/api/v1/review",
    tags=["Review"]
)


# GET ALL REVIEWS
@router.get("/", response_model=List[schemas.ReviewOut])
async def getAllReviews(db : MongoClient = Depends(get_db)):
    reviews = list(db["reviews"].find())
    for review in reviews:
        review['_id'] = str(review['_id'])  # Convert ObjectId to string for JSON serialization
    return reviews


# GET REVIEW BY ID
@router.get("/{id}", response_model=schemas.ReviewOut)
async def getReview(id : str, db: MongoClient = Depends(get_db)):
    review = db["reviews"].find_one({"_id" : ObjectId(id)})

    if review == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    # Convert ObjectId to string for JSON serialization
    review['_id'] = str(review['_id'])
    return review


# POST A REVIEW
@router.post("/", response_model=schemas.ReviewOut)
async def postReview(data : schemas.Review, db: MongoClient = Depends(get_db)):
    """
        This function allows a customer to post a review and the user to check if the review is valid so it can be viewed by the public
        If is_approved is false, then the it should only be able to be viewed by the admin
    """
    try:
        result = db["reviews"].insert_one(data.model_dump())
        inserted_item = db["reviews"].find_one({"_id": ObjectId(result.inserted_id)})
        inserted_item['_id'] = str(inserted_item['_id'])
        return inserted_item
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error inserting item: {str(e)}")

# DELETE A REVIEW
@router.delete("/{id}")
async def deleteReview(id : str, db: MongoClient = Depends(get_db)):
    result = db["reviews"].delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    return  {"Message": f"Review with id of {id} has been deleted successfully"}


# Update a review
@router.put("/{id}", response_model=schemas.ReviewOut)
async def updateReview(data: schemas.ReviewUpdate, id : str, db : MongoClient = Depends(get_db)):
    review = db["reviews"].find_one({"_id" : ObjectId(id)})

    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with id of {id} was not found")

    # Prepare the update data
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}

    # Update the review in the database
    db["reviews"].update_one({"_id": ObjectId(id)}, {"$set": update_data})

    # Retrieve the updated review
    updated_review = db["reviews"].find_one({"_id": ObjectId(id)})
    updated_review['_id'] = str(updated_review['_id'])  # Convert ObjectId to string for JSON serialization

    return schemas.ReviewOut(**updated_review)  # Return the updated review


# APPROVE REVIEW
@router.put("/approve/{id}")
async def approveReview(id: str, current_user: Annotated[schemas.User, Depends(ouath2.get_current_active_user)], data : schemas.ReviewApprove, db : MongoClient = Depends(get_db)):
    review = db["reviews"].find_one({"_id" : ObjectId(id)})
    
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Review with id of {id} was not found")
    print(data)
    db["reviews"].update_one({"_id": ObjectId(id)}, {"$set": data.model_dump()})
    return {"Message": f"Review with id of {id} has been approved successfully"}
    

@router.post("/")
async def sendMail(db: MongoClient = Depends(get_db)):
   """
        send email to reviewer for further discussions
    """
   pass