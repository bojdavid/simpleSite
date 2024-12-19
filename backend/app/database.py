from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from .config import Settings

uri = f"mongodb+srv://{Settings.database_username}:{Settings.database_password}@simplesite.bx8ax.mongodb.net/?retryWrites=true&w=majority&appName=SimpleSite"


def get_db():
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[Settings.database_name] 
    try:
        yield db
    finally:
        client.close()
