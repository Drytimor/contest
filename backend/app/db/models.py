import enum
from .database import settings
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import (
    ForeignKey, PrimaryKeyConstraint, UniqueConstraint, ForeignKeyConstraint, CheckConstraint,
    MetaData, Column
)
from typing import Optional
from sqlalchemy.types import Integer, String, DateTime, Boolean, Text, NUMERIC, Time
import datetime
from sqlalchemy import Enum as sqlalchemyEnum


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Mode(str, enum.Enum):
    full = 'full',
    partial = 'partial'


class Base(DeclarativeBase):


    metadata = MetaData(
        naming_convention=naming_convention
    )
    type_annotation_map = {
        Mode: sqlalchemyEnum(Mode, native_enum=False),
    }


class Users(Base):
    __tablename__ = 'users'

    id: Mapped['int'] = mapped_column(primary_key=True)
    username: Mapped['str'] = mapped_column(String(255), unique=True)
    password: Mapped['str'] = mapped_column(String(255), unique=True)
    is_superuser: Mapped['bool'] = mapped_column()

    def __repr__(self):
        return f'<User>:{self.username}'


class Competitions(Base):
    __tablename__ = 'competitions'

    id: Mapped['int'] = mapped_column(primary_key=True)
    name: Mapped['str'] = mapped_column(String(255), unique=True)
    date: Mapped['datetime.datetime'] = mapped_column(DateTime(timezone=True))
    description: Mapped[Optional['str']] = mapped_column(Text(), nullable=True)
    contribution: Mapped[list['Contributions']] = relationship(
        back_populates='competition', cascade='all, delete'
    )
    complex: Mapped[list['Complexes']] = relationship(
        back_populates='competition', cascade='all, delete'
    )
    participant: Mapped[list['Participants']] = relationship(
        back_populates='competition', cascade='all, delete'
    )

    def __repr__(self):
        return f"<Competition:{self.name}>-id:{self.id}"


class Contributions(Base):
    __tablename__ = 'contributions'
    __table_args__ = (
        PrimaryKeyConstraint('competition_id', 'mode'),
        CheckConstraint(
            Column('mode').in_([Mode.partial.value, Mode.full.value]),
            name='contribution_mode'
        )
    )
    competition_id: Mapped['int'] = mapped_column(
        ForeignKey('competitions.id', ondelete='CASCADE')
    )
    competition: Mapped['Competitions'] = relationship(back_populates='contribution')
    payment: Mapped[list['Payments']] = relationship(
        back_populates='contribution', cascade='all, delete'
    )
    mode: Mapped['Mode']
    price: Mapped['float'] = mapped_column(NUMERIC(10, 2))


    def __repr__(self):
        return f"<Contribution:{self.competition_id}>-mode:{self.mode}"


class Participants(Base):
    __tablename__ = 'participants'

    id: Mapped['int'] = mapped_column(primary_key=True)
    competition_id: Mapped['int'] = mapped_column(
        ForeignKey('competitions.id', ondelete='CASCADE')
    )
    competition: Mapped['Competitions'] = relationship(back_populates='participant')
    payment: Mapped[list['Payments']] = relationship(
        back_populates='participant', cascade='all, delete'
    )
    qualifying_video: Mapped[list['QualifyingVideos']] = relationship(
        back_populates='participant', cascade='all, delete'
    )
    result: Mapped[list['Results']] = relationship(
        back_populates='participant', cascade='all, delete'
    )
    fullname: Mapped['str'] = mapped_column(String(255))
    email: Mapped['str'] = mapped_column(String(255), unique=True)
    is_qualified: Mapped['bool'] = mapped_column(default=False)
    is_arrived: Mapped['bool'] = mapped_column(default=False)


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        UniqueConstraint('competition_id', 'participant_id', 'mode'),
        ForeignKeyConstraint(
            ['competition_id', 'mode'],
            ['contributions.competition_id', 'contributions.mode'],
            ondelete='CASCADE'
        ),
        CheckConstraint(
            Column('mode').in_([Mode.partial.value, Mode.full.value]),
            name='payment_mode'
        )
    )
    id: Mapped['int'] = mapped_column(primary_key=True)
    participant_id: Mapped['int'] = mapped_column(
        ForeignKey('participants.id', ondelete='CASCADE')
    )
    participant: Mapped['Participants'] = relationship(back_populates='payment')
    competition_id: Mapped['int']
    mode: Mapped['Mode']
    contribution: Mapped['Contributions'] = relationship(back_populates='payment')
    pay_datetime: Mapped['datetime'] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )


class Complexes(Base):
    __tablename__ = 'complexes'
    __table_args__ = (
        UniqueConstraint('id', 'competition_id', 'name'),
    )

    id: Mapped['int'] = mapped_column(primary_key=True)
    name: Mapped['str'] = mapped_column(String(255))
    competition_id: Mapped['int'] = mapped_column(
        ForeignKey('competitions.id', ondelete='CASCADE'),
    )
    competition: Mapped['Competitions'] = relationship(back_populates='complex')
    qualifying_video: Mapped[list['QualifyingVideos']] = relationship(
        back_populates='complex', cascade='all, delete'
    )
    result: Mapped[list['Results']] = relationship(
        back_populates='complex', cascade='all, delete'
    )
    description: Mapped['str'] = mapped_column(Text())
    is_qualifying: Mapped['bool'] = mapped_column()
    start_time: Mapped['datetime.time'] = mapped_column(Time(timezone=True))
    end_time: Mapped['datetime.time'] = mapped_column(Time(timezone=True))


class QualifierStatus(str, enum.Enum):
    qualified = 'qualified'
    unqualified = 'unqualified'


class QualifyingVideos(Base):
    __tablename__ = 'qualifying_videos'
    __table_args__ = (
        PrimaryKeyConstraint('complex_id', 'participant_id'),
    )
    complex_id: Mapped['int'] = mapped_column(
        ForeignKey('complexes.id', ondelete='CASCADE')
    )
    complex: Mapped['Complexes'] = relationship(back_populates='qualifying_video')
    participant_id: Mapped['int'] = mapped_column(
        ForeignKey('participants.id', ondelete='CASCADE')
    )
    participant: Mapped['Participants'] = relationship(back_populates='qualifying_video')
    video_url: Mapped['str'] = mapped_column(String(255))
    qualifier_status: Mapped['QualifierStatus'] = mapped_column(default=QualifierStatus.unqualified.value)


class ViewResult(str, enum.Enum):
    kg = 'kg',
    meters = 'meters'
    min = 'min'
    reps = 'reps'
    cl = 'cl'


class Results(Base):
    __tablename__ = 'results'
    __table_args__ = (
        PrimaryKeyConstraint(
            'complex_id', 'participant_id'
        ),
    )
    complex_id: Mapped['int'] = mapped_column(
        ForeignKey('complexes.id', ondelete='CASCADE')
    )
    complex: Mapped['Complexes'] = relationship(back_populates='result')
    participant_id: Mapped['int'] = mapped_column(
        ForeignKey('participants.id', ondelete='CASCADE')
    )
    participant: Mapped['Participants'] = relationship(back_populates='result')
    view: Mapped['ViewResult']
    result: Mapped['str'] = mapped_column(String(255))