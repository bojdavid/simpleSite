from fastapi import APIRouter

router = APIRouter(
    prefix="/adminAuth",
    tags=["Admin"]
)




@router.post("/login")
async def login():
    pass

@router.post("signUp")
async def createUser():
    pass

@router.get("/")
async def getUser():
    pass

@router.delete("/")
async def deleteUser():
    pass

@router.put("/")
async def updateUser():
    pass