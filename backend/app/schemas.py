from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone


#services
class Services(BaseModel):
    service : str
    description : str
    image_data: bytes = Field(None, alias="image")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

class ServiceCreate(Services):
    pass

class ServiceUpdate(BaseModel):
    service : str
    description : str
    image_data: bytes = Field(None, alias="image")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  

class ServiceOut(Services):
    id : str  = Field(..., alias="_id") 
    
    
#Review
class Review(BaseModel):
    email : EmailStr
    rating : int = Field(..., gt=0, lt=6)
    #profile_picture : bytes = Field(None, alias="image")
    review_text : str
    is_approved : bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    


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
 
    
class Bio(BaseModel):
    name : str
    email : EmailStr
    profile_picture : bytes = Field(None, alias="image")
    description : str #give us an introduction or a motto
    about : str    #tell us about your bussiness
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class BioOut(Bio):
    id : str  = Field(..., alias="_id")

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
    #id : str  = Field(..., alias="_id")
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = {"extra": "forbid"}

class UserInDB(User):
    hashed_password: str