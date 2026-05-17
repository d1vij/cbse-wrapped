from typing import Literal

from compiler.models.CleanedResultModel import (
    CleanedSchoolResultModel,
    CleanedStudentResultModel,
    PrimarySubjectModel,
    SkillSubjectModel,
    StudentSubjectsModel,
)
from compiler.models.RawResponseModels import (
    RawResultResponseModel,
    RawSchoolResultJsonModel,
    RawStudentResultModel,
    SubjectIndexes,
)
from compiler.utils.parse import parse_int


def clean_primary_subject(
    raw: RawStudentResultModel, idx: SubjectIndexes
) -> PrimarySubjectModel | None:

    subject_id = getattr(raw, f"SUB{idx}")
    if subject_id == "":
        return None

    return PrimarySubjectModel(
        subject_id=parse_int(subject_id, 0),
        passed=True if getattr(raw, f"PF{idx}") == "P" else False,
        grade=getattr(raw, f"GR{idx}"),
        marks_theory=parse_int(getattr(raw, f"MRK{idx}1"), 0),
        marks_practicals=parse_int(getattr(raw, f"MRK{idx}2"), 0),
        marks_total=parse_int(getattr(raw, f"MRK{idx}3"), 0),
        marks_total_words=getattr(raw, f"MRK{idx}3_WRDS"),
    )


def clean_secondary_subject(
    raw: RawStudentResultModel, idx: Literal["1", "2", "3"]
) -> SkillSubjectModel:
    return SkillSubjectModel(
        subject_id=int(getattr(raw, f"ISUB{idx}")), grade=getattr(raw, f"IGR{idx}")
    )


def clean_student_result(
    result_response: RawResultResponseModel,
) -> CleanedStudentResultModel:
    raw = result_response.data
    return CleanedStudentResultModel(
        rollnumber=int(raw.RROLL),
        name_candidate=raw.CNAME,
        name_mother=raw.MNAME,
        name_father=raw.FNAME,
        sex=raw.SEX,
        catagory=False if raw.CAT == "" else raw.CAT,
        candidate_type="regular" if raw.REG == "E" else "private",
        cleared_all_subjects=True if raw.RES == "PASS" else False,
        result_status="pass" if raw.RESULT == "PASS" else "compartment",
        compartment_subject_codes=raw.COMPTT,
        total_marks=int(raw.TMRK),
        primary_subjects=StudentSubjectsModel.model_validate(
            {
                "s1": clean_primary_subject(raw, "1"),
                "s2": clean_primary_subject(raw, "2"),
                "s3": clean_primary_subject(raw, "3"),
                "s4": clean_primary_subject(raw, "4"),
                "s5": clean_primary_subject(raw, "5"),
                "s6": clean_primary_subject(raw, "6"),
            }
        ),
        secondary_subjects=False
        if raw.IS_SKILL == "N"
        else [
            clean_secondary_subject(raw, "1"),
            clean_secondary_subject(raw, "2"),
            clean_secondary_subject(raw, "3"),
        ],
    )


def clean_school_result(raw: RawSchoolResultJsonModel) -> CleanedSchoolResultModel:
    if len(raw.success) == 0:
        raise ValueError("No successfull results found for the passed school.")

    # rather than passing additional options,
    # we'll infer school meta from a student object
    student = raw.success[0].data

    return CleanedSchoolResultModel(
        school_number=int(student.SCH),
        school_name=student.SCH_NAME,
        centre_number=int(student.CENT),
        date_of_results=student.DOD,
        students_without_result=len(raw.failed),
        # consume the iterator so that we can serialize it
        students=list(map(clean_student_result, raw.success)),
    )
