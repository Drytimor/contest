from fastapi import HTTPException, status, Depends
from typing import Annotated
from ...db.database import SessionDep
from ...db.models import Competitions
from sqlalchemy.exc import NoResultFound


async def get_current_competition(
        competition_id: int, session: SessionDep
):
    try:
        competition = session.get_one(Competitions, competition_id)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Competition not with ID: {competition_id} not found'
        )
    return competition

CurrentCompetition = Annotated[Competitions, Depends(get_current_competition)]