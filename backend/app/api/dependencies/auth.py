from fastapi import HTTPException, status, Depends
from pydantic import ValidationError
from ..schemas.auth import TokenPayload
from ...core.security import verify_password, settings
from sqlalchemy.exc import NoResultFound
from ..crud.auth import get_user_from_db, Session
from ...db.database import SessionDep
from ...db.models import Users
from jose import JWTError, jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from ..log import Logger


log = Logger(__name__, 'app/base.log').logger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def identify_user(
        username: str, session: Session
):
    user = get_user_from_db(
        username=username, session=session
    )
    return user



def authenticate_user(
        username: str, password: str, session: Session
):
    user = identify_user(username, session)
    if not user or not verify_password(password, user.password):
        return False

    return user


def get_current_user(
        token: TokenDep, session: SessionDep
):
    try:
        payload = jwt.decode(
            token, settings.TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(sub=payload.get('sub'))
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Could not validate credentials'
        )
    user = identify_user(token_data.sub, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

CurrentUser = Annotated[Users, Depends(get_current_user)]
CurrentUserDepends = Depends(get_current_user)

