import datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional
from src.praktyki.helpers import now


class Company(BaseModel):
    id: UUID
    name: str
    info: str | None
    nip: str  # number; but might be international


class Internship(BaseModel):
    id: UUID
    student_id: UUID  # person_id, not the studentid from WD

    # computed as InternshipPeriod are being closed
    total_days: int
    start_at: datetime.date
    closed_at: datetime.date | None


class Role(IntEnum):
    STUDENT = 0
    WSIZ_SUPERVISOR = 1
    ZOP = 2
    ADMIN = 3


class Person(BaseModel):
    # all people in the system
    person_id: UUID  # primary key
    name: str
    email: str  # unique (can be fetched by this; used for login)
    phone: str | None
    password: str | None = Field(exclude=True)  # Exclude password from being serialized by .dict() method

    # WSIZ identifiers
    studentid: Optional[int] | None
    album: Optional[str] | None
    wykladowcaid: Optional[int] | None
    # external identifiers
    company_id: Optional[UUID] | None
    uid_in_company: Optional[UUID] | None

    roles: list[Role]
    active: bool = True


class Signable(BaseModel):
    """
    All signables will potentially have their frozen version stored in
    DocumentDB, and the signature structure associated with it.

    Marker class.
    """
    id: UUID


class FrameworkAgreement(Signable):
    company_id: UUID

    active: bool
    created_at: datetime.date
    file_data: bytes | None  # pdf
    file_name: str | None  # pdf


class CV(BaseModel):
    id: UUID
    student_id: UUID
    data: bytes | None  # pdf
    filename: str | None  # pdf  -- add this field to DB and all methods that need it
    created_at: datetime.date
    immutable: bool = False  # once attached to application -- immutable


class Application(Signable):
    """
    An InternshipPeriod is opened once Application is fully signed.

    Created by student,
    - approved(signed) by any WsizSupervisor
    - accepted(signed) by ZOP
    """
    framework_agreement_id: UUID
    company_id: UUID
    cv_id: UUID | None
    student_id: UUID
    created_at: datetime.date | None = Field(default=now())  # should actually be filled
    # todo: add "active" (if period created --> active=False)
    # todo: add "rejected" (can be done by SUP or ZOP --> won't appear anymore [not so critical])

    info: str  # to be extended


class InternshipAgreement(Signable):
    student_id: UUID
    application_id: UUID
    company_id: UUID
    created_at: datetime.datetime



class PeriodStatus(IntEnum):
    FINALIZED = 0
    OPENED = 1  # on create
    STUDENT_DONE = 2  # by student, allows ZOP to approve/close it (with signatures and survey)
    ZOP_APPROVED = 3  # aka EVALUATED and signed by ZOP


class Period(Signable):
    """
    On close, signed by supervisor.
    """
    internship_id: UUID
    # repeated id's for easier access
    student_id: UUID
    company_id: UUID
    status: PeriodStatus

    opened_at: datetime.datetime
    expected_end: datetime.datetime  # no InternshipDay can be created with date after this date


class PeriodFinalReport(Signable):
    period_id: UUID
    period_days: list[UUID]  # once final report exists, these days will not be editable anymore;
    total_days: int
    # repeated id's for easier access
    student_id: UUID
    company_id: UUID
    created_at: datetime.datetime


class WaiverStatus(IntEnum):
    ACCEPTED = 0
    PROPOSED = 1
    DECLINED = 2


class InternshipWaiver(Signable):
    """
    PROPOSED - signed by student
    ACCEPTED/DECLINED -- signed by supervisor
    """
    internship_id: UUID
    status: WaiverStatus


class Day(BaseModel):
    id: UUID  # allows for a view: internships.wsi.edu.pl/days/iday_id --- with details & edits
    period_id: UUID
    date_at: datetime.date
    immutable: bool = False

    project: str  # very "light" grouping of tasks; fully controlled by student (checked by ZOP)
    tasks: list[str]  # opisowe... ? ok? (else Task(iday_id, str, ...))


class Survey(Signable):
    """
    On "submit", the survey is signed by ZOP.
    """
    internship_period_id: UUID
    final_score: float
    submitted_at: datetime.date | None
    submitted: bool


class SurveyCategory(IntEnum):
    WIEDZA = 0
    UMIEJETNOSCI = 1
    SPOLECZNE = 2


class SurveyAnswer(BaseModel):
    id: UUID
    survey_id: UUID
    category: SurveyCategory
    question: str  # copied from SurveyQuestion on creation
    score: int


class SurveyQuestion(BaseModel):
    """
    Prepared beforehand by WSIZ.
    """
    id: UUID
    category: SurveyCategory
    question: str
