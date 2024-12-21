from fastapi import FastAPI
from .routes import adminAuth,bio,review,services
from .database import get_db

app = FastAPI()

try:
    get_db()
    print("Database connection successful")

    app.include_router(adminAuth.router)
    app.include_router(bio.router)
    app.include_router(review.router)
    app.include_router(services.router) 

    #print(get_db().list_database_names())

except Exception as e:
    print(e)

@app.get("/")
async def root():
    return {"message": "Hello World"}


 # Add this line
