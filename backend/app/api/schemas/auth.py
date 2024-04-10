from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated
from ...core.security import get_password_hash


HashPassword = Annotated[str, AfterValidator(get_password_hash)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None


class UserBase(BaseModel):
    username: str
    is_superuser: bool


class UserCreate(UserBase):
    password: HashPassword


class UserRead(UserBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
