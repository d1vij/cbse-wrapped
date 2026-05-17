# contains the models representing a student's results after getting cleaned and normalized
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .RawResponseModels import Grade, Sex
from .SubjectModel import SubjectId


class PrimarySubjectModel(BaseModel):
    # did the student pass in this subjec
    subject_id: SubjectId
    passed: bool
    grade: Grade
    marks_theory: int
    marks_practicals: int
    marks_total: int
    marks_total_words: str


class SkillSubjectModel(BaseModel):
    subject_id: SubjectId
    grade: Grade


# keep this as an dict instead of list so that 
# later on it becomes easier to form a dataframe out of it
class StudentSubjectsModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    s1: PrimarySubjectModel = Field(alias="1")
    s2: PrimarySubjectModel = Field(alias="2")
    s3: PrimarySubjectModel = Field(alias="3")
    s4: PrimarySubjectModel = Field(alias="4")
    s5: PrimarySubjectModel = Field(alias="5")
    s6: PrimarySubjectModel | None = Field(alias="6")


class CleanedStudentResultModel(BaseModel):
    rollnumber: int
    name_candidate: str
    name_father: str
    name_mother: str

    sex: Sex
    catagory: Union[str, Literal[False]]
    candidate_type: Literal["regular", "private"]

    primary_subjects: StudentSubjectsModel
    # secondary/internal subjects like work experience
    skill_subjects: Union[list[SkillSubjectModel], Literal[False]]

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
    students_without_result: int
    students: list[CleanedStudentResultModel]
