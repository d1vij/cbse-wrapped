# contains the models representing a student's results after getting cleaned and normalized
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict

from .RawResponseModels import Grade, Sex
from .SubjectModel import SubjectId, StreamModel, StreamId


class PrimarySubjectModel(BaseModel):
    # did the student pass in this subject
    subject_id: SubjectId
    passed: bool
    grade: Grade
    marks_theory: int
    marks_practicals: int
    marks_total: int
    marks_total_words: str


class SecondarySubjectModel(BaseModel):
    subject_id: SubjectId
    grade: Grade


# keep this as an dict instead of list so that
# later on it becomes easier to form a dataframe out of it
class StudentSubjectsModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    sub_1: PrimarySubjectModel
    sub_2: PrimarySubjectModel
    sub_3: PrimarySubjectModel
    sub_4: PrimarySubjectModel
    sub_5: PrimarySubjectModel
    sub_6: PrimarySubjectModel | None


class CleanedStudentResultModel(BaseModel):
    rollnumber: int
    name_candidate: str
    name_father: str
    name_mother: str

    sex: Sex
    catagory: Union[str, Literal[False]]
    candidate_type: Literal["regular", "private"]
    stream_id: StreamId

    primary_subjects: StudentSubjectsModel

    # secondary/internal subjects like work experience
    secondary_subjects: list[SecondarySubjectModel]

    cleared_all_subjects: bool
    result_status: Literal["pass", "compartment"]
    compartment_subject_codes: str
    total_marks: int


# import re
# from pydantic import field_validator
# @field_validator("date_of_results")
# @classmethod
# def validate_date_of_results(cls, v: str) -> str:
#     if not re.fullmatch(r"\d{2}/\d{2}\d{4}", v):
#         raise ValueError("date_of_results must match the format DD/MM/YYYY")
#     return v
class CleanedSchoolResultModel(BaseModel):
    school_number: int
    centre_number: int
    school_name: str
    date_of_results: str
    subjects_available: dict[SubjectId, str]
    streams: dict[StreamId, StreamModel]
    students_without_result: int
    students: list[CleanedStudentResultModel]
