from pydantic import BaseModel, Field, EmailStr

#services
class Services(BaseModel):
    service : str
    description : str
    image_data: bytes = Field(None, alias="image")

class ServiceCreate(Services):
    pass

class ServiceOut(Services):
    id : str  = Field(..., alias="_id") 


#Review
class Review(BaseModel):
    email : EmailStr
    stars : int = Field(..., gt=0, lt=6)
    profile_picture : bytes = Field(None, alias="image")
    comment : str
    
class Bio(BaseModel):
    profile_picture : bytes = Field(None, alias="image")
    description : str
    about : str    