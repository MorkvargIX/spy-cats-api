from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db_session
from app.models.mission import Mission
from app.models.target import Target
from app.models.spy_cat import SpyCat
from app.schemas.mission import MissionCreate, MissionRead, MissionAssign
from app.schemas.target import TargetUpdate, TargetOut

router = APIRouter(
    prefix="/missions",
    tags=["Missions"],
)


@router.post("/", response_model=MissionRead)
async def create_mission(
    data: MissionCreate,
    db: AsyncSession = Depends(get_db_session),
):
    mission = Mission(is_completed=False)

    for target in data.targets:
        mission.targets.append(
            Target(
                name=target.name,
                country=target.country,
                notes=target.notes,
                is_completed=False,
            )
        )

    db.add(mission)
    await db.commit()

    result = await db.execute(
        select(Mission)
        .options(selectinload(Mission.targets))
        .where(Mission.id == mission.id)
    )
    mission = result.scalar_one()

    return mission


@router.post("/{mission_id}/assign", response_model=MissionRead)
async def assign_cat_to_mission(
    mission_id: int,
    payload: MissionAssign,
    db: AsyncSession = Depends(get_db_session),
):
    mission = await db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")

    if mission.cat_id is not None:
        raise HTTPException(400, "Mission already assigned")

    cat = await db.get(SpyCat, payload.cat_id)
    if not cat:
        raise HTTPException(404, "Cat not found")

    stmt = select(Mission).where(Mission.cat_id == cat.id)
    existing_mission = await db.scalar(stmt)

    if existing_mission:
        raise HTTPException(400, "Cat already has a mission")

    mission.cat_id = cat.id
    await db.commit()

    stmt = (
        select(Mission)
        .where(Mission.id == mission.id)
        .options(selectinload(Mission.targets))
    )

    mission = await db.scalar(stmt)
    return mission


@router.delete(
    "/{mission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_mission(
    mission_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    mission = await db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")

    if mission.cat_id is not None:
        raise HTTPException(
            400,
            "Cannot delete mission assigned to a cat",
        )

    await db.delete(mission)
    await db.commit()


@router.patch("/targets/{target_id}", response_model=TargetOut)
async def update_target(
    target_id: int,
    payload: TargetUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(Target)
        .where(Target.id == target_id)
        .options(
            selectinload(Target.mission)
            .selectinload(Mission.targets)
        )
    )

    target = (await db.scalars(stmt)).first()
    if not target:
        raise HTTPException(404, "Target not found")

    if target.is_completed or target.mission.is_completed:
        raise HTTPException(
            400,
            "Cannot update notes of a completed target or mission",
        )

    if payload.notes is not None:
        target.notes = payload.notes

    if payload.is_completed is not None:
        target.is_completed = payload.is_completed

    if all(t.is_completed for t in target.mission.targets):
        target.mission.is_completed = True

    await db.commit()
    await db.refresh(target)
    return target



@router.get("", response_model=list[MissionRead])
async def list_missions(
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(Mission)
        .options(selectinload(Mission.targets))
    )

    result = await db.scalars(stmt)
    missions = result.all()
    return missions


@router.get("/{mission_id}", response_model=MissionRead)
async def get_mission(
    mission_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    stmt = (
        select(Mission)
        .where(Mission.id == mission_id)
        .options(selectinload(Mission.targets))
    )

    mission = await db.scalar(stmt)
    if not mission:
        raise HTTPException(404, "Mission not found")
    return mission
