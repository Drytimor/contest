from sqlalchemy.orm import Session, contains_eager, aliased, selectinload, joinedload
from sqlalchemy import select, text, update, delete
from fastapi import HTTPException
from ..schemas.competitions import (
    CompetitionCreate, CompetitionUpdate, ContributionCreate, ContributionUpdate, ComplexesCreate, ResultsCreate
)
from ..dependencies.competition import CurrentCompetition
from ...db.models import Competitions, Contributions, Complexes, Results
from ..log import Logger

log = Logger(__name__, 'app/base.log').logger

def create_competition_from_db(
        session: Session, competition: CompetitionCreate
):
    db_obj = Competitions(**competition.dict())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_competition_from_db(
        competition_id: int, session: Session
):
    result = session.scalars(
        select(Competitions)
        .options(joinedload(Competitions.contribution))
        .filter_by(id=competition_id)
    ).unique().one()

    return result

def get_all_competition_from_db(session:Session):

    result = session.scalars(
        select(Competitions)
    ).all()

    return result

def update_competition_from_db(
        current_competition: CurrentCompetition, updated_competition_data:CompetitionUpdate,
        session: Session
):
    result = session.scalars(
        update(Competitions)
        .where(Competitions.id==current_competition.id)
        .values(**updated_competition_data.model_dump(exclude_unset=True))
        .returning(Competitions)
    ).one()

    session.commit()

    return result


def delete_competition_from_db(
        current_competition:CurrentCompetition, session: Session
):
    session.delete(current_competition)
    session.commit()
    return True


def create_contribution_from_db(
        competition_id: CurrentCompetition, contribution: ContributionCreate,
        session: Session
):
    result = session.scalars(
        insert(Contributions)
        .values(
            competition_id=competition_id,
            **contribution.model_dump(exclude_unset=True),
            )
        .returning(Contributions)
    ).one()

    session.commit()

    return result


def get_contributions_from_db(
        competition_id: int, session: Session
):
    result = session.scalars(
        select(Contributions)
        .where(Contributions.competition_id==competition_id)
    ).all()

    return result


def update_contribution_from_db(
        competition_id: int, contribution_mode:str,
        contribution_in: ContributionUpdate, session:Session
):
    result = session.scalars(
        update(Contributions)
        .where(
            Contributions.competition_id==competition_id,
            Contributions.mode==contribution_mode
        )
        .values(**contribution_in.model_dump(exclude_unset=True))
        .returning(Contributions)
    ).one()

    return result


def delete_contribution_from_db(
        competition_id: int, contribution_mode:str, session:Session
):
    session.scalars(
        delete(Contributions)
        .where(Contributions.competition_id==competition_id,
               Contributions.mode==contribution_mode)
        .returning(Contributions.competition_id)
    ).one()

def create_complex_from_db(
        competition_id:int, complex_data:ComplexesCreate, session:Session
):
    complex = Complexes(competition_id=competition_id, **complex_data.dict())
    session.add(complex)
    session.commit()
    session.refresh(complex)

    return complex


def get_all_complexes_from_db(
    competition_id:int, session:Session
):
    complexes = session.scalars(
        select(Complexes)
        .where(Complexes.competition_id==competition_id)
    ).all()

    return complexes


def create_result_complex_from_db(
    complex_id: int, participant_id: int, session:Session,
    result_data: ResultsCreate
):
    result = Results(
        complex_id=complex_id, participant_id=participant_id,
        **result_data.dict()
    )
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def get_all_result_complexes_from_db(
    complex_id: int, session:Session
):
    complexes_result = session.scalars(
        select(Results)
        .where(Results.complex_id==complex_id)
    ).all()

    return complexes_result