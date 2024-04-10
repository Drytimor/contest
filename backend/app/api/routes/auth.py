from fastapi import APIRouter, Depends, HTTPException, status
from ...db.database import SessionDep
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from ..dependencies.auth import authenticate_user, CurrentUser
from ..schemas.auth import Token, UserCreate, UserRead
from ..crud.auth import create_user_from_db
from ...core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from ..log import Logger


log = Logger(__name__, 'app/base.log').logger


auth_router = APIRouter(
    tags=['Authentication']
)
user_router = APIRouter(
    prefix="/users",
    tags=["user"]
)


FormLoginDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@auth_router.post('/token')
async def login(
        form_data: FormLoginDep, session:SessionDep
)-> Token:
    user = authenticate_user(
        username=form_data.username, password=form_data.password, session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({'sub': user.username})
    return Token(access_token=access_token, token_type="bearer")


@user_router.post('/', response_model=UserRead)
async def create_user(
        user_in: UserCreate, session: SessionDep
):
    try:
        user = create_user_from_db(
            user_in=user_in, session=session
        )
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc.args)
        )
    return user


@user_router.get("/me", response_model=UserRead)
async def get_users(current_user: CurrentUser):
    return current_user