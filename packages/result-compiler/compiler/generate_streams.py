import pandas as pd

from compiler.models.CleanedResultModel import (
    CleanedStudentResultModel,
)
from compiler.models.SubjectModel import (
    StreamId,
    StreamJsonModel,
    StreamModel,
    SubjectId,
)
from compiler.utils.json_utils import read_from

streams = StreamJsonModel.model_validate_json(read_from("streams.json"))


def generate_school_streams(
    students: list[CleanedStudentResultModel],
) -> dict[StreamId, StreamModel]:
    found: list[StreamId] = []
    school_streams: dict[StreamId, StreamModel] = {}

    for student in students:
        if (student.stream_id not in found) and (
            (meta := get_stream_metadata(student.stream_id)) is not None
        ):
            found.append(student.stream_id)
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
def resolve_stream(subjects_series: pd.Series[SubjectId]) -> StreamId | None:
    stream: StreamModel
    for stream in streams.root:
        if stream.subjects_series.equals(
            subjects_series.sort_values().reset_index(drop=True)
        ):
            return stream.stream_id
    return None


def get_stream_metadata(stream_id: StreamId) -> StreamModel | None:
    stream: StreamModel
    for stream in streams.root:
        if stream.stream_id == stream_id:
            return stream

    return None
