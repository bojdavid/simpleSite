from fastapi import APIRouter

router = APIRouter(
    prefix="/bio",
    tags=["Bio"]
)