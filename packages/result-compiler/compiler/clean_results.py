# cleans the raw result response by doing type conversions,
# feild eliminations, and metadata compilation which require
# the raw result response object


import pandas as pd

from compiler.models.CleanedResultModel import (
    CleanedPrimarySubjectModel,
    CleanedSchoolResultModel,
    CleanedStudentResultModel,
    SecondarySubjectModel,
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
from compiler.utils.stream_utils import generate_school_streams, resolve_stream


def clean_primary_subject(
    raw: RawStudentResultModel, idx: SubjectIndexes
) -> CleanedPrimarySubjectModel | None:

    subject_id = getattr(raw, f"SUB{idx}")

    if subject_id == "":
        return None

    return CleanedPrimarySubjectModel(
        subject_id=subject_id,
        passed=True if getattr(raw, f"PF{idx}") == "P" else False,
        grade=getattr(raw, f"GR{idx}"),
        # parsing the marks as integers because CBSE rounds off all marks to ints
        marks_theory=parse_int(getattr(raw, f"MRK{idx}1"), 0),
        marks_practicals=parse_int(getattr(raw, f"MRK{idx}2"), 0),
        marks_total=parse_int(getattr(raw, f"MRK{idx}3"), 0),
        marks_total_words=getattr(raw, f"MRK{idx}3_WRDS"),
    )


def clean_secondary_subject(
    raw: RawStudentResultModel, idx: int
) -> SecondarySubjectModel | None:

    subject_id = getattr(raw, f"ISUB{idx}")
    if subject_id == "":
        return None

    return SecondarySubjectModel(subject_id=subject_id, grade=getattr(raw, f"IGR{idx}"))


def clean_student_result(
    result_response: RawResultResponseModel,
) -> CleanedStudentResultModel:
    raw = result_response.data

    secondary_subjects: list[SecondarySubjectModel] = []
    for idx in range(1, 4):
        subject = clean_secondary_subject(raw, idx)
        if subject:
            secondary_subjects.append(subject)

    primary_subjects = StudentSubjectsModel.model_validate(
        {
            "sub_1": clean_primary_subject(raw, "1"),
            "sub_2": clean_primary_subject(raw, "2"),
            "sub_3": clean_primary_subject(raw, "3"),
            "sub_4": clean_primary_subject(raw, "4"),
            "sub_5": clean_primary_subject(raw, "5"),
            "sub_6": clean_primary_subject(raw, "6"),
        }
    )

    subjects_series = pd.Series(
        [
            primary_subjects.sub_1.subject_id,
            primary_subjects.sub_2.subject_id,
            primary_subjects.sub_3.subject_id,
            primary_subjects.sub_4.subject_id,
            primary_subjects.sub_5.subject_id,
            primary_subjects.sub_6.subject_id if primary_subjects.sub_6 else None,
        ]
    ).dropna()

    stream_id = resolve_stream(subjects_series)

    if stream_id is None:
        raise ValueError(
            f"Couldnt resolve streams for subjects with code {primary_subjects}\nStudent's subject codes include {subjects_series.sort_values().to_list()}"
        )

    return CleanedStudentResultModel(
        roll_number=int(raw.RROLL),
        name_candidate=raw.CNAME,
        name_mother=raw.MNAME,
        name_father=raw.FNAME,
        sex=raw.SEX,
        stream_id=stream_id,
        catagory=False if raw.CAT == "" else raw.CAT,
        candidate_type="regular" if raw.REG == "E" else "private",
        cleared_all_subjects=True if raw.RES == "PASS" else False,
        result_status="pass" if raw.RESULT == "PASS" else "compartment",
        compartment_subject_codes=raw.COMPTT,
        total_marks=int(raw.TMRK),
        total_primary_subjects=subjects_series.size,
        primary_subjects=primary_subjects,
        secondary_subjects=secondary_subjects,
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
    any_student = raw.success[0].data

    students = list(map(clean_student_result, raw.success))
    return CleanedSchoolResultModel(
        school_number=int(any_student.SCH),
        school_name=any_student.SCH_NAME,
        centre_number=int(any_student.CENT),
        date_of_results=any_student.DOD,
        students_without_result=len(raw.failed),
        subjects_available=generate_subject_list(raw.success),
        streams=generate_school_streams(students),
        # consume the iterator so that we can serialize it
        students=students,
    )
