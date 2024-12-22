from passlib.context import CryptContext
from .schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    """if username in db:
        user_dict = db[username]
    """
    user = db["users"].find_one({"email" : username})
    user["_id"]
    #return user
    return UserInDB(**user)
    

def authenticate_user(db, username: str, password: str):
    user = db["users"].find_one({"email" : username})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

