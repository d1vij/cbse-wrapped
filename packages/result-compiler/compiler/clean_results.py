# cleans the raw result response by doing type conversions,
# feild eliminations, and metadata compilation which require
# the raw result response object


from typing import Literal, Union

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
from compiler.models.SubjectModel import SubjectId
from compiler.utils.parse import parse_int


def clean_primary_subject(
    raw: RawStudentResultModel, idx: SubjectIndexes
) -> PrimarySubjectModel | None:

    subject_id = getattr(raw, f"SUB{idx}")

    if subject_id == "":
        return None

    return PrimarySubjectModel(
        subject_id=subject_id,
        passed=True if getattr(raw, f"PF{idx}") == "P" else False,
        grade=getattr(raw, f"GR{idx}"),
        marks_theory=parse_int(getattr(raw, f"MRK{idx}1"), 0),
        marks_practicals=parse_int(getattr(raw, f"MRK{idx}2"), 0),
        marks_total=parse_int(getattr(raw, f"MRK{idx}3"), 0),
        marks_total_words=getattr(raw, f"MRK{idx}3_WRDS"),
    )


def clean_skill_subject(
    raw: RawStudentResultModel, idx: int
) -> SkillSubjectModel | None:

    subject_id = getattr(raw, f"ISUB{idx}")
    if subject_id == "":
        return None

    return SkillSubjectModel(subject_id=subject_id, grade=getattr(raw, f"IGR{idx}"))


def clean_student_result(
    result_response: RawResultResponseModel,
) -> CleanedStudentResultModel:
    raw = result_response.data

    skill_subjects: Union[Literal[False], list[SkillSubjectModel]]
    if raw.IS_SKILL == "N":
        skill_subjects = False
    else:
        skill_subjects = []
        for idx in range(1, 4):
            subject = clean_skill_subject(raw, idx)
            if subject:
                skill_subjects.append(subject)

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
        skill_subjects=skill_subjects,
    )


def generate_subject_list(
    students: list[RawResultResponseModel],
) -> dict[SubjectId, str]:
    subjects: dict[SubjectId, str] = {}
    for student in students:
        for idx in range(1, 7):
            sub_code = getattr(student.data, f"SUB{idx}")
            if sub_code != "":
                subjects[sub_code] = getattr(student.data, f"SNAME{idx}")

        for idx in range(1, 4):
            sub_code = getattr(student.data, f"ISUB{idx}")
            if sub_code != "":
                subjects[sub_code] = getattr(student.data, f"ISNAME{idx}")

    return subjects


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
        subjects_available=generate_subject_list(raw.success),
        # consume the iterator so that we can serialize it
        students=list(map(clean_student_result, raw.success)),
    )
