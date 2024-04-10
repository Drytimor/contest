from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete
from ..schemas.participants import ParticipantsCreate, QualificationCreate
from ...db.models import Participants, Payments, Mode, QualifyingVideos


def register_participant_for_qualifying(
        competition_id: int, participant_data: ParticipantsCreate, session: Session
):
    participant = Participants(
        competition_id=competition_id, **participant_data.dict()
    )
    session.add(participant)
    payment = Payments(mode=Mode.partial.value, competition_id=competition_id)
    participant.payment.append(payment)
    session.commit()
    session.refresh(participant)
    return participant


def get_all_participants_from_db(
    competition_id: int, session: Session
):
    participants = session.scalars(
        select(Participants)
        .where(Participants.competition_id==competition_id)
    ).all()

    return participants


def create_qualification_video_from_db(
    complex_id: int, participant_id: int,
    qualifying_data: QualificationCreate, session: Session
):
    qualifying_video = QualifyingVideos(
        complex_id=complex_id, participant_id=participant_id,
        **qualifying_data.dict()
    )
    session.add(qualifying_video)
    session.commit()
    session.refresh(qualifying_video)
    return qualifying_video