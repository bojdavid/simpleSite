from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import datetime, timezone
from bson import ObjectId
from typing import Optional


#services
class Services(BaseModel):
    service : str
    description : str
    image: Optional[bytes] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    isApproved: bool =False
    
    

class ServiceCreate(Services):
    pass

class ServiceUpdate(BaseModel):
    service : str
    description : str
    image: Optional[bytes] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    isApproved: bool =False
  

class ServiceOut(Services):
    id : str  = Field(..., alias="_id") 
    service : str
    description : str
    image: Optional[bytes] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    isApproved: bool =False

class ServiceApprove(BaseModel):
    isApproved : bool

    
#Review
class Review(BaseModel):
    email : EmailStr
    clientName: str
    rating : int = Field(..., gt=0, lt=6)
    #profile_picture : bytes = Field(None, alias="image")
    text : str
    approved : bool = False
    date: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    userId : str

    def validate_user_id(cls, v):
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(v)
        except Exception:
            raise ValueError('Invalid user ID format')

    """class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str} 
    """
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        #extra = "forbid" #If you want to forbid extra parameters
    ) 
    


class ReviewOut(Review):
    id : str  = Field(..., alias="_id")     
 
class ReviewUpdate(BaseModel):
    email : EmailStr
    rating : int = Field(..., gt=0, lt=6)
    #profile_picture : bytes = Field(None, alias="image")
    review_text : str
    is_approved : bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
 
class ReviewApprove(BaseModel):
    approved : bool


#------ BIO --------    
class Bio(BaseModel):
    name : str
    email : EmailStr
    profile_picture : Optional[bytes] = None
    description : str #give us an introduction or a motto
    about : str    #tell us about your bussiness
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BioOut(Bio):
    id : str  = Field(..., alias="_id")
    userId : str

# FORM
class LoginData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"} #don't allow extra fields



# TOKEN
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

# USER
class User(BaseModel):
    id : str  = Field(..., alias="_id")
    email : EmailStr
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    disabled: bool | None = None
    

class UserCreate(BaseModel):
    fullname: str 
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    disabled: bool | None = None
    model_config = {"extra": "forbid"}

"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {"extra": "forbid"}
"""

class UserInDB(User):
    hashed_password: str