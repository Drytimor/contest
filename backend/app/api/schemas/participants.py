from pydantic import BaseModel, ConfigDict
from ...db.models import QualifierStatus

class ParticipantsBase(BaseModel):
    fullname: str
    email: str


class ParticipantsCreate(ParticipantsBase):
    pass


class ParticipantsUpdate(ParticipantsBase):
    pass


class ParticipantsRead(ParticipantsBase):

    model_config = ConfigDict(from_attributes=True)

    id: int
    competition_id: int
    is_qualified: bool
    is_arrived: bool


class QualificationBase(BaseModel):
    video_url: str


class QualificationCreate(QualificationBase):
    pass


class QualificationRead(QualificationBase):

    model_config = ConfigDict(from_attributes=True)

    complex_id: int
    qualifier_status: QualifierStatus


