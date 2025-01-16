from pymongo.mongo_client import MongoClient
from app.config import Settings
from app.database import get_db
from app.main import app

uri = "mongodb://localhost:27017/"

def override_get_db():
    conn = MongoClient(uri)
    db = conn[Settings.database_name] 
    try:
        yield db
    finally:
        conn.close()

app.dependency_overrides[get_db] = override_get_db