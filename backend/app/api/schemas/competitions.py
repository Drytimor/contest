import datetime
from pydantic import BaseModel, ConfigDict
from ..log import Logger
import sys
from ...db.models import Mode, ViewResult
from datetime import time


logger = Logger(__name__, 'app/base.log').logger


class CompetitionBase(BaseModel):
    name: str
    date: datetime.datetime
    description: str | None = None


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionRead(CompetitionBase):

    model_config = ConfigDict(from_attributes=True)

    id: int




class CompetitionReadWithJoin(CompetitionRead):

    model_config = ConfigDict(from_attributes=True)

    contribution: list['ContributionRead'] = []



class CompetitionUpdate(CompetitionBase):
    pass


class ContributionBase(BaseModel):
    price: float


class ContributionCreate(ContributionBase):
    mode: Mode


class ContributionRead(ContributionCreate):

    model_config = ConfigDict(from_attributes=True)

    competition_id: int



class ContributionUpdate(ContributionBase):
    pass



class ComplexesBase(BaseModel):
    name: str
    description: str
    is_qualifying: bool
    start_time: time
    end_time: time


class ComplexesCreate(ComplexesBase):
    pass


class ComplexesUpdate(ComplexesBase):
    pass

class ComplexesRead(ComplexesUpdate):

    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int


class ResultsBase(BaseModel):
    view: ViewResult
    result: str


class ResultsCreate(ResultsBase):
    pass


class ResultsRead(ResultsBase):

    model_config = ConfigDict(from_attributes=True)

    complex_id: int
    participant_id: int