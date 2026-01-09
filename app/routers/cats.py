from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session


router = APIRouter(
    prefix="/cats",
    tags=["Spy Cats"],
)


@router.get("/")
async def list_cats(
    session: AsyncSession = Depends(get_db_session),
):
    return []