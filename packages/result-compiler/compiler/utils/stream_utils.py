from typing import Callable

import pandas as pd

from compiler.models.CleanedResultModel import (
    CleanedStudentResultModel,
)
from compiler.models.CompiledResultModel import CompiledStudentResultModel
from compiler.models.SubjectModel import (
    StreamId,
    StreamJsonModel,
    StreamModel,
    SubjectId,
)
from compiler.utils.json_utils import read_from
from compiler.utils.memoize import memoize

streams = StreamJsonModel.model_validate_json(read_from("streams.json"))


def generate_school_streams(
    students: list[CleanedStudentResultModel],
) -> dict[StreamId, StreamModel]:
    """
    Returns all the streams available in a particular school from its student's metadata
    """

    school_streams: dict[StreamId, StreamModel] = {}

    for student in students:
        if (student.stream_id not in school_streams) and (
            (meta := get_stream_metadata(student.stream_id)) is not None
        ):
            school_streams[student.stream_id] = meta

    return school_streams


# NOTE: Callee fn
# subjects_series = (
#     pd.Series(
#         [
#             subjects.s1.subject_id,
#             subjects.s2.subject_id,
#             subjects.s3.subject_id,
#             subjects.s4.subject_id,
#             subjects.s5.subject_id,
#             subjects.s6.subject_id if subjects.s6 else None,
#         ]
#     )
#     .drop_na()
# )
@memoize
def resolve_stream(subjects_series: pd.Series[SubjectId]) -> StreamId | None:
    """
    Resolves and Returns a `StreamId` which corresponds to the subject series passed. Returns `None` if its unable to resolve any stream.
    """
    stream: StreamModel
    for stream in streams.root:
        if stream.subjects_series.equals(
            subjects_series.sort_values().reset_index(drop=True)
        ):
            return stream.stream_id
    return None


@memoize
def get_stream_metadata(stream_id: StreamId) -> StreamModel | None:
    """
    Returns `StreamModel` for the given `StreamId`. Returns `None` if not found.
    """
    for stream in streams.root:
        if stream.stream_id == stream_id:
            return stream
    return None


@memoize
def get_streams_having_subject(subject_id: SubjectId) -> tuple[StreamId, ...]:
    """
    Returns a tuple of `StreamId` which include the provided `SubjectId`
    """
    streams_with_subject: list[StreamId] = []
    for stream in streams.root:
        if subject_id in stream.subjects:
            streams_with_subject.append(stream.stream_id)

    return tuple(streams_with_subject)


def get_students_having_stream(
    stream_id: StreamId,
    students: list[CleanedStudentResultModel] | list[CompiledStudentResultModel],
    *,
    exclude_when: Callable[[CleanedStudentResultModel], bool] | None = None,
) -> list[CleanedStudentResultModel]:
    filtered: list[CleanedStudentResultModel] = []

    for student in students:
        if student.stream_id == stream_id:
            if exclude_when is None or not exclude_when(student):
                filtered.append(student)

    return filtered
