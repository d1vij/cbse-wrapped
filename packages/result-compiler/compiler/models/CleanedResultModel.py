# contains the models representing a student's results after getting cleaned and normalized
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel

from .RawResponseModels import Grade, Sex
from .SubjectModel import StreamId, StreamModel, SubjectId
from .Units import NonZeroInt


class CleanedPrimarySubjectModel(BaseModel):
    # did the student pass in this subject
    subject_id: SubjectId
    passed: bool
    grade: Grade
    # CBSE rounds off all marks to nearest integers
    marks_theory: NonZeroInt
    marks_practicals: NonZeroInt
    marks_total: NonZeroInt
    marks_total_words: str


class SecondarySubjectModel(BaseModel):
    subject_id: SubjectId
    grade: Grade


# keep this as an dict instead of list so that
# later on it becomes easier to form a dataframe out of it
class StudentSubjectsModel[T_SubjectModel = CleanedPrimarySubjectModel](BaseModel):
    sub_1: T_SubjectModel
    sub_2: T_SubjectModel
    sub_3: T_SubjectModel
    sub_4: T_SubjectModel
    sub_5: T_SubjectModel
    sub_6: T_SubjectModel | None


class CleanedStudentResultModel(BaseModel):
    roll_number: NonZeroInt
    name_candidate: str
    name_father: str
    name_mother: str

    sex: Sex
    catagory: Union[str, Literal[False]]
    candidate_type: Literal["regular", "private"]
    stream_id: StreamId

    total_primary_subjects: NonZeroInt
    primary_subjects: StudentSubjectsModel

    # secondary/internal subjects like work experience
    secondary_subjects: list[SecondarySubjectModel]

    cleared_all_subjects: bool
    result_status: Literal["pass", "compartment"]
    compartment_subject_codes: str
    total_marks: NonZeroInt


# import re
# from pydantic import field_validator
# @field_validator("date_of_results")
# @classmethod
# def validate_date_of_results(cls, v: str) -> str:
#     if not re.fullmatch(r"\d{2}/\d{2}\d{4}", v):
#         raise ValueError("date_of_results must match the format DD/MM/YYYY")
#     return v
class CleanedSchoolResultModel(BaseModel):
    school_number: NonZeroInt
    centre_number: NonZeroInt
    school_name: str
    date_of_results: str
    subjects_available: dict[SubjectId, str]
    streams: dict[StreamId, StreamModel]
    students_without_result: NonZeroInt
    students: list[CleanedStudentResultModel]
