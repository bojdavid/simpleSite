from typing import Annotated, List
from fastapi import APIRouter, Form
from .. import schemas, utils, ouath2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from ..database import get_db
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime, timedelta, timezone
from ..config import Settings


router = APIRouter(
    prefix="/api/v1/adminAuth",
    tags=["Admin"]
)


@router.post("/login/")
async def login( form_data: Annotated[OAuth2PasswordRequestForm, Depends()],  db: MongoClient = Depends(get_db)) -> schemas.Token:
    #print(form_data.password)
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    #print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings.access_token_expire_minutes)

    #Data that would be placed in the token
    token_data = {"sub": user["email"], "userId": str(user["_id"]), "name":str(user["fullname"])}
    access_token = ouath2.create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/signUp", response_model=schemas.User)
async def createUser( user: Annotated[schemas.UserCreate, Form()], db: MongoClient = Depends(get_db)):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    
    try:
        db["users"].create_index([('email', ASCENDING)], unique=True)
        result  = db["users"].insert_one(user.model_dump())
        inserted_item = db["users"].find_one({"_id": ObjectId(result.inserted_id)})
        inserted_item['_id'] = str(inserted_item['_id'])
        return inserted_item
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


    

@router.get("/", response_model=List[schemas.User])
async def getAllUsers(db : MongoClient = Depends(get_db)):
    users = list(db["users"].find())
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string for JSON serialization
    return users


@router.delete("/")
async def deleteUser():
    pass

@router.put("/")
async def updateUser():
    pass