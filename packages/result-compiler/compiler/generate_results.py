# TODO: optimize
import pandas as pd
from typing_extensions import cast

from compiler.models.CleanedResultModel import (
    CleanedPrimarySubjectModel,
    CleanedSchoolResultModel,
    CleanedStudentResultModel,
)
from compiler.models.CompiledResultModel import (
    CompiledPrimarySubjectModel,
    CompiledSchoolResultModel,
    CompiledStudentResultModel,
    CompiledStudentSubjectsModel,
    CompliedStreamModel,
)
from compiler.models.SubjectModel import StreamId, StreamModel
from compiler.models.Units import NonZeroFloat, NonZeroInt
from compiler.utils.percentile import (
    calculate_percentile,
    get_score_matrix,
    get_score_percentile_matrix,
)
from compiler.utils.stream_utils import get_students_having_stream


def generate_primary_subject_result(
    self_subject: CleanedPrimarySubjectModel | None,
    *,
    self_student: CleanedStudentResultModel,
    students: list[CleanedStudentResultModel],
    percentile_matrix: pd.DataFrame,
    score_matrix: pd.DataFrame,
) -> CompiledPrimarySubjectModel | None:
    if self_subject is None:
        return None

    percentile_all_streams = cast(
        float, percentile_matrix.at[self_student.roll_number, self_subject.subject_id]
    )

    students_same_stream = [
        s.roll_number
        for s in get_students_having_stream(
            self_student.stream_id,
            students,
            exclude_when=lambda s: s.roll_number == self_student.roll_number,
        )
    ]

    subject_ser: pd.Series[NonZeroInt] = score_matrix[
        self_subject.subject_id
    ].sort_values()

    rank_same_stream = (
        subject_ser[subject_ser.index.isin(students_same_stream)]
        .gt(self_subject.marks_total)
        .sum()
        + 1
    )

    rank_all_streams = subject_ser.gt(self_subject.marks_total).sum() + 1

    return CompiledPrimarySubjectModel(
        **self_subject.model_dump(),
        # since total marks are out of 100
        percentage=self_subject.marks_total,
        percentile_all_streams=percentile_all_streams,
        rank_same_stream=rank_same_stream,
        rank_all_streams=rank_all_streams,
    )


def generate_student_result(
    student: CleanedStudentResultModel,
    students: list[CleanedStudentResultModel],
    score_matrix: pd.DataFrame,
    percentile_matrix: pd.DataFrame,
    rank_same_stream: NonZeroInt,
    rank_all_streams: NonZeroInt,
) -> CompiledStudentResultModel:

    compiled_primary_subjects = CompiledStudentSubjectsModel.model_validate(
        {
            subject_key: generate_primary_subject_result(
                self_student=student,
                self_subject=cleaned_subject,
                score_matrix=score_matrix,
                students=students,
                percentile_matrix=percentile_matrix,
            )
            for (subject_key, cleaned_subject) in student.primary_subjects
        }
    )

    total_score_series = pd.Series({s.roll_number: s.total_marks for s in students})
    same_stream_students = [
        s.roll_number for s in get_students_having_stream(student.stream_id, students)
    ]
    same_stream_score_series = total_score_series[
        total_score_series.index.isin(same_stream_students)
    ]

    return CompiledStudentResultModel(
        **student.model_dump(exclude={"primary_subjects"}),
        percentage=student.total_marks / 5, # cbse only considers 5 subjects when calculating percentage
        primary_subjects=compiled_primary_subjects,
        percentile_same_stream=calculate_percentile(
            student.total_marks, same_stream_score_series
        ),
        percentile_all_streams=calculate_percentile(
            student.total_marks, total_score_series
        ),
        rank_same_stream=rank_same_stream,
        rank_all_streams=rank_all_streams,
    )


def get_student_percentage_ser(
    students: list[CompiledStudentResultModel],
) -> pd.Series:
    records: list[NonZeroFloat] = []
    for student in students:
        records.append(student.percentage)
    return pd.Series(records)


def complile_stream(
    stream: StreamModel, students: list[CompiledStudentResultModel]
) -> CompliedStreamModel:

    stream_students = get_students_having_stream(stream.stream_id, students)
    percentage_ser = get_student_percentage_ser(stream_students)

    return CompliedStreamModel(
        **stream.model_dump(),
        students_total=percentage_ser.size,
        students_passed=sum(1 for s in stream_students if s.result_status == "pass"),
        percentage_mean=percentage_ser.mean(),
        percentage_median=percentage_ser.median(),
        percentage_max=percentage_ser.max(),
        percentage_min=percentage_ser.min(),
    )


def build_rank_map(
    score_series: pd.Series,
    method: str = "min",
) -> dict[NonZeroInt, NonZeroInt]:
    """
    Returns {roll_number: rank} in descending order of score.
    """
    return cast(
        dict[NonZeroInt, NonZeroInt],
        (score_series.rank(method="first", ascending=False).astype(int).to_dict()),
    )


def generate_school_result(
    school_results: CleanedSchoolResultModel,
) -> CompiledSchoolResultModel:
    score_matrix = get_score_matrix(school_results)
    percentile_matrix = get_score_percentile_matrix(school_results, score_matrix)

    # --- build total-score rank maps ONCE ---
    total_score_ser = pd.Series(
        {s.roll_number: s.total_marks for s in school_results.students}
    )
    rank_all_streams_map = build_rank_map(total_score_ser)

    # per-stream rank maps, also built once
    rank_same_stream_map: dict[NonZeroInt, int] = {}
    for stream_id, _ in school_results.streams.items():
        stream_rolls = {
            s.roll_number for s in school_results.students if s.stream_id == stream_id
        }
        stream_ser = total_score_ser[total_score_ser.index.isin(stream_rolls)]
        rank_same_stream_map.update(build_rank_map(stream_ser))

    students = [
        generate_student_result(
            student=s,
            score_matrix=score_matrix,
            percentile_matrix=percentile_matrix,
            students=school_results.students,
            rank_all_streams=rank_all_streams_map[s.roll_number],
            rank_same_stream=rank_same_stream_map[s.roll_number],
        )
        for s in school_results.students
    ]
    percentage_ser = get_student_percentage_ser(students)

    streams: dict[StreamId, CompliedStreamModel] = {
        stream_id: complile_stream(stream, students)
        for (stream_id, stream) in school_results.streams.items()
    }

    return CompiledSchoolResultModel(
        **school_results.model_dump(exclude={"students", "streams"}),
        students=students,
        streams=streams,
        percentage_mean=percentage_ser.mean(),
        percentage_median=percentage_ser.median(),
        percentage_max=percentage_ser.max(),
        percentage_min=percentage_ser.min(),
    )
