from fastapi import APIRouter, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from ..schemas.participants import ParticipantsRead, ParticipantsCreate, QualificationCreate
from ...db.database import SessionDep
from typing import Annotated
from ..crud.participants import (
    register_participant_for_qualifying, get_all_participants_from_db, create_qualification_video_from_db
)


participant_router = APIRouter(
    prefix="/participants",
    tags=["Participants"]
)
qualifying_router = APIRouter(
    prefix="/qualifying",
    tags=["Qualifying"]
)

CompetitionId = Annotated[int, Query(ge=1)]
ComplexId = Annotated[int, Query(ge=1)]
ParticipantId = Annotated[int, Query(ge=1)]


@participant_router.post("/", response_model=ParticipantsRead)
async def register_participant_for_qualifying_stage(
     competition_id: CompetitionId, participant_data: ParticipantsCreate, session: SessionDep
):
    try:
        participant = register_participant_for_qualifying(
            competition_id=competition_id, participant_data=participant_data, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return participant

@participant_router.get('/', response_model=list[ParticipantsRead])
async def get_all_participants(
        competition_id: CompetitionId, session:SessionDep
):
    try:
        participants = get_all_participants_from_db(
            competition_id=competition_id, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return participants

@qualifying_router.post('/')
async def create_participant_qualification_video(
   complex_id: ComplexId, participant_id: ParticipantId,
   qualifying_data: QualificationCreate, session: SessionDep
):
    try:
        qualification_result = create_qualification_video_from_db(
            complex_id=complex_id, participant_id=participant_id,
            qualifying_data=qualifying_data, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return qualification_result