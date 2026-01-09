from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db_session
from app.models.spy_cat import SpyCat
from app.schemas.spy_cat import (
    SpyCatCreate,
    SpyCatRead,
    SpyCatUpdate,
)
from app.services.cat_api import is_valid_breed

router = APIRouter(
    prefix="/cats",
    tags=["Spy Cats"],
)


@router.post(
    "",
    response_model=SpyCatRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_spy_cat(
    payload: SpyCatCreate,
    db: AsyncSession = Depends(get_db_session),
):
    is_valid = await is_valid_breed(payload.breed)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid cat breed",
        )
    cat_data = payload.model_dump()
    cat_data["breed"] = cat_data["breed"].title()

    cat = SpyCat(**cat_data)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


@router.get(
    "",
    response_model=list[SpyCatRead],
)
async def list_spy_cats(
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(select(SpyCat))
    return result.scalars().all()


@router.get(
    "/{cat_id}",
    response_model=SpyCatRead,
)
async def get_spy_cat(
    cat_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    cat = await db.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found",
        )
    return cat


@router.patch(
    "/{cat_id}",
    response_model=SpyCatRead,
)
async def update_spy_cat_salary(
    cat_id: int,
    payload: SpyCatUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    cat = await db.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found",
        )

    cat.salary = payload.salary
    await db.commit()
    await db.refresh(cat)
    return cat


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_spy_cat(
    cat_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    cat = await db.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spy cat not found",
        )

    await db.delete(cat)
    await db.commit()

