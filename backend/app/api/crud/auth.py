from sqlalchemy.orm import Session
from ...db.models import Users
from sqlalchemy import insert, select


def create_user_from_db(
        user_in, session: Session
):
    result = session.scalars(
        insert(Users)
        .values(user_in.model_dump(exclude_unset=True))
        .returning(Users)
    ).one()

    session.commit()

    return result


def get_user_from_db(
        username: str, session: Session
):
    result = session.scalars(
        select(Users)
        .where(Users.username == username)
    ).first()

    return result


