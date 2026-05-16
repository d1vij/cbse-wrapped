from typing import Literal

from compiler.models.CleanedResultModel import (
    CleanedStudentResultModel,
    PrimarySubjectModel,
    SkillSubjectModel,
    StudentSubjectsModel,
)
from compiler.models.RawResponseModels import RawStudentResultModel, SubjectIndexes


def clean_primary_subject(
    raw: RawStudentResultModel, idx: SubjectIndexes
) -> PrimarySubjectModel:
    return PrimarySubjectModel(
        subject_id=int(getattr(raw, f"SUB{idx}")),
        passed=True if getattr(raw, f"PF{idx}") == "P" else False,
        grade=getattr(raw, f"GR{idx}"),
        marks_theory=int(getattr(raw, f"MRK{idx}1")),
        marks_practicals=int(getattr(raw, f"MRK{idx}2")),
        marks_total=int(getattr(raw, f"MRK{idx}3")),
        marks_total_words=getattr(raw, f"MRK{idx}"),
    )


def clean_secondary_subject(
    raw: RawStudentResultModel, idx: Literal["1", "2", "3"]
) -> SkillSubjectModel:
    return SkillSubjectModel(
        subject_id=int(getattr(raw, f"ISUB{idx}")), grade=getattr(raw, f"IGR{idx}")
    )


def clean_student_result(
    raw: RawStudentResultModel,
) -> CleanedStudentResultModel:

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
                "1": clean_primary_subject(raw, "1"),
                "2": clean_primary_subject(raw, "2"),
                "3": clean_primary_subject(raw, "3"),
                "4": clean_primary_subject(raw, "4"),
                "5": clean_primary_subject(raw, "5"),
                "6": clean_primary_subject(raw, "6"),
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

