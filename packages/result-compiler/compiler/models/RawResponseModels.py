# copy of packages/scraper/schemas/cbseresultschema.ts
# Contains the model for raw result response which
# the digilocker API returns

from __future__ import annotations

import re
from typing import Literal
from pydantic import BaseModel, field_validator, UUID4

SubjectIndexes = Literal["1", "2", "3", "4", "5", "6"]

# CBSE 9-point grade scale
Grade = Literal["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E"]
Sex = Literal["M", "F"]

# Grade or empty for unused optional subjects
GradeOrEmpty = Literal["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E", ""]

# Subject result flag
# "P"  = Pass
# "RT" = Result withheld
# ""   = Unused subject slot
SubjectPassFlag = Literal["P", "RT", ""]

# Reusable yes/no flag
YNFlag = Literal["Y", "N"]


# Normalized DigiLocker CBSE result schema
class RawStudentResultModel(BaseModel):
    # Admission ID
    ADMN_ID: str

    # Student name
    CNAME: str

    # Father name
    FNAME: str

    # Mother name
    MNAME: str

    # Student gender
    SEX: Sex

    # Class / standard
    CLASS: str

    # Academic session
    SESSION: str

    # Exam month
    MONTH: str

    # Supplementary exam month, usually empty
    MONTH_L: str

    # Result declaration date
    DOD: str

    # Exam year
    YEAR: str

    # Issuing organization
    ORGID: Literal["CBSE"]

    # Exam center code
    CENT: str

    # School code
    SCH: str

    # School name
    SCH_NAME: str

    # Student type
    # "X" = Private
    # "E" = Regular
    REG: Literal["X", "E"]

    # Whether the result is publicly published
    PUBLISHED: YNFlag

    # Record version
    VERSION: str

    # Last updated timestamp
    MODIFIED_ON: str

    # Roll number
    RROLL: str

    # Roll + year composite key
    RROLL_YEAR: str

    # DigiLocker document URI
    URI: str

    # Internal storage key
    SK: str

    # Internal GSI partition key
    GSI_PK: str

    # Internal GSI sort key
    GSI_SK: str

    # Main result status
    # "PASS" = Cleared all subjects
    # "COMP" = Compartment
    RES: Literal["PASS", "COMP"]

    # Secondary result label
    # Empty for compartment cases
    RESULT: Literal["PASS", ""]

    # Compartment subject codes
    COMPTT: str

    # Total marks
    TMRK: str

    # Category code or empty for General
    CAT: str

    # Registered under NCHMCT stream
    IS_NCHMCT: YNFlag

    NCHMCT_1: str
    NCHMCT_2: str

    # Registered under NSE
    IS_NSE: YNFlag

    NSE_1: str
    NSE_2: str

    # Has a skill subject
    IS_SKILL: YNFlag

    SKILL_1: str
    SKILL_2: str

    # Subject names and codes
    # Empty string means subject not taken
    SNAME1: str
    SUB1: str

    SNAME2: str
    SUB2: str

    SNAME3: str
    SUB3: str

    SNAME4: str
    SUB4: str

    SNAME5: str
    SUB5: str

    SNAME6: str
    SUB6: str

    # Per-subject pass flags
    PF1: SubjectPassFlag
    PF2: SubjectPassFlag
    PF3: SubjectPassFlag
    PF4: SubjectPassFlag
    PF5: SubjectPassFlag
    PF6: SubjectPassFlag

    # Per-subject grades
    # Slot 6 may be empty
    GR1: Grade
    GR2: Grade
    GR3: Grade
    GR4: Grade
    GR5: Grade
    GR6: GradeOrEmpty

    # Marks:
    # MRKxy
    # x = subject index (1–6)
    # y = 1 theory, 2 practical, 3 total
    MRK11: str
    MRK12: str
    MRK13: str
    MRK13_WRDS: str

    MRK21: str
    MRK22: str
    MRK23: str
    MRK23_WRDS: str

    MRK31: str
    MRK32: str
    MRK33: str
    MRK33_WRDS: str

    MRK41: str
    MRK42: str
    MRK43: str
    MRK43_WRDS: str

    MRK51: str
    MRK52: str
    MRK53: str
    MRK53_WRDS: str

    MRK61: str
    MRK62: str
    MRK63: str
    MRK63_WRDS: str

    # Internal/co-scholastic subjects
    ISNAME1: str
    ISNAME2: str
    ISNAME3: str

    ISUB1: str
    ISUB2: str
    ISUB3: str

    # Internal subject grades
    IGR1: Grade
    IGR2: Grade
    IGR3: Grade

    @field_validator("SESSION")
    @classmethod
    def validate_session(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("SESSION must match YYYY-YYYY")
        return v

    @field_validator("DOD")
    @classmethod
    def validate_dod(cls, v: str) -> str:
        if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", v):
            raise ValueError("DOD must match DD/MM/YYYY")
        return v

    @field_validator("YEAR")
    @classmethod
    def validate_year(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}", v):
            raise ValueError("YEAR must be a 4-digit string")
        return v

    @field_validator("MODIFIED_ON")
    @classmethod
    def validate_modified_on(cls, v: str) -> str:
        if not v.endswith("Z"):
            v = f"{v}Z"
        # Basic ISO 8601 timestamp check
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z", v):
            raise ValueError("MODIFIED_ON must be a valid ISO timestamp")
        return v

    @field_validator("RROLL")
    @classmethod
    def validate_rroll(cls, v: str) -> str:
        if not re.fullmatch(r"\d+", v):
            raise ValueError("RROLL must be numeric")
        return v

    @field_validator("RROLL_YEAR")
    @classmethod
    def validate_rroll_year(cls, v: str) -> str:
        if not re.fullmatch(r"\d+_\d{4}", v):
            raise ValueError("RROLL_YEAR must match {digits}_{YYYY}")
        return v

    @field_validator("TMRK")
    @classmethod
    def validate_tmrk(cls, v: str) -> str:
        if not re.fullmatch(r"\d+", v):
            raise ValueError("TMRK must be numeric")
        return v


class RawResultResponseModel(BaseModel):
    data: RawStudentResultModel

    # API processing time in seconds
    duration_sec: float

    # Request UUID
    request_id: UUID4

    # HTTP status code
    status: Literal[200]


class FailedResultResponseModel(BaseModel):
    status: Literal["failed"]
    student_name: str
    roll_number: str


class RawSchoolResultJsonModel(BaseModel):
    success: list[RawResultResponseModel]
    failed: list[FailedResultResponseModel]
