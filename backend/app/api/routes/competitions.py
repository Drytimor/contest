from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from typing import Annotated
from ..dependencies.competition import CurrentCompetition
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from ..log import Logger
from ..schemas.competitions import (
    CompetitionCreate, CompetitionReadWithJoin, CompetitionRead, CompetitionUpdate, ContributionRead, ContributionUpdate,
    ContributionCreate, ComplexesCreate, ComplexesRead, ComplexesUpdate, ResultsCreate, ResultsRead
)
from ...db.database import SessionDep
from ...db.models import Mode
from ..crud.competitions import (
    create_competition_from_db, get_competition_from_db, get_all_competition_from_db, update_competition_from_db,
    delete_competition_from_db, create_contribution_from_db, get_contributions_from_db, update_contribution_from_db,
    delete_contribution_from_db, get_all_complexes_from_db, create_result_complex_from_db, get_all_result_complexes_from_db,
    create_complex_from_db
)


competition_router = APIRouter(
    prefix='/competitions',
    tags=['Competition'],
)
contribution_router = APIRouter(
    prefix='/contributions',
    tags=['Contribution']
)
complex_router = APIRouter(
    prefix='/complexes',
    tags=['Complexes']
)
result_router = APIRouter(
    prefix='/results',
    tags=['Results']
)

log = Logger(__name__, 'app/base.log').logger


CompetitionId = Annotated[int, Query(ge=1)]
ComplexId = Annotated[int, Query(ge=1)]
ParticipantId = Annotated[int, Query(ge=1)]

@competition_router.post('/', response_model=CompetitionRead)
async def create_competition(
        competition_in: CompetitionCreate, session: SessionDep
):
    try:
        competition = create_competition_from_db(
            competition=competition_in, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return competition


@competition_router.get('/', response_model=list[CompetitionRead])
async def get_all_competitions(session: SessionDep):
    competitions = get_all_competition_from_db(session=session)
    return competitions


@competition_router.get('/{competition_id}', response_model=CompetitionReadWithJoin)
async def get_competition(
        competition_id: Annotated[int, Path(ge=1)], session: SessionDep
):
    try:
        competition = get_competition_from_db(
            competition_id=competition_id, session=session
        )
    except NoResultFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc.args)
        )
    return competition


@competition_router.put('/{competition_id}', response_model=CompetitionRead)
async def update_competition(
        current_competition: CurrentCompetition, updated_competition_data: CompetitionUpdate,
        session: SessionDep
):
    competition = update_competition_from_db(
        current_competition=current_competition, updated_competition_data=updated_competition_data,
        session=session
    )
    return competition


@competition_router.delete('/')
async def delete_competition(
        current_competition: CurrentCompetition, session: SessionDep
):
    competition = delete_competition_from_db(
        current_competition=current_competition, session=session
    )
    if competition:
        return {'status':f'{status.HTTP_200_OK}',
                'message': f'Competition deleted {current_competition.id}'}




@contribution_router.post('/', response_model=ContributionRead)
async def create_contribution(
        competition_id: CompetitionId, contribution_in: ContributionCreate,
        session: SessionDep
):
        try:
            contribution = create_contribution_from_db(
                competition_id=competition_id, contribution=contribution_in,
                session=session,
            )
        except IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.args)
            )
        return contribution


@contribution_router.get('/', response_model=list[ContributionRead])
async def get_contribution(
        competition_id: CompetitionId, session: SessionDep
):
    contribution = get_contributions_from_db(
        competition_id=competition_id, session=session
    )
    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contribution with competition_id {competition_id} not found"
        )
    return contribution


@contribution_router.put('/', response_model=ContributionRead)
async def update_contribution(
        competition_id: CompetitionId, contribution_mode: Mode,
        contribution_in: ContributionUpdate, session: SessionDep,
):
    try:
        contribution = update_contribution_from_db(
            competition_id=competition_id, contribution_mode=contribution_mode,
            contribution_in=contribution_in, session=session
        )
    except NoResultFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc.args)
        )
    return contribution


@contribution_router.delete('/')
async def delete_contribution(
        competition_id: CompetitionId,contribution_mode: Mode, session: SessionDep
):
    try:
        delete_contribution_from_db(
            competition_id=competition_id, contribution_mode=contribution_mode,
            session=session
        )
    except NoResultFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc.args)
        )
    return {'message': 'Contribution deleted'}



@complex_router.post('/', response_model=ComplexesRead)
async def create_complex(
        competition_id: CompetitionId, complex_data: ComplexesCreate, session: SessionDep
):
    try:
        complex = create_complex_from_db(
            competition_id=competition_id, complex_data=complex_data, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return complex


@complex_router.get('/', response_model=list[ComplexesRead])
async def get_all_complexes(
    competition_id: CompetitionId, session:SessionDep
):
    try:
        complexes = get_all_complexes_from_db(
            competition_id=competition_id, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return complexes


@result_router.post('/', response_model=ResultsRead)
async def create_result_complex(
    complex_id: ComplexId, participant_id: ParticipantId,
    result_data: ResultsCreate ,session: SessionDep
):
    try:
        result_complex = create_result_complex_from_db(
            complex_id=complex_id, participant_id=participant_id,
            result_data=result_data, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return result_complex


@result_router.get('/', response_model=list[ResultsRead])
async def get_all_result_complexes(
    complex_id: ComplexId, session: SessionDep
):
    try:
        complexes = get_all_result_complexes_from_db(
            complex_id=complex_id, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.orig)
        )
    return complexes