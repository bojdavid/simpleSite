from fastapi import FastAPI
from .routes import about,admin,bio,review,services

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(about.router)
app.include_router(admin.router)
app.include_router(bio.router)
app.include_router(review.router)
app.include_router(services.router)  # Add this line
