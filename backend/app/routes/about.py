from fastapi import APIRouter

router = APIRouter(
    prefix="/about",
    tags=["About"]
)

@router.get("/")
async def getAbout():
    return {"message":"This is the about section"}