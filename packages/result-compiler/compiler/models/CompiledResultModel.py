# all models will extend their corresponding cleaned
# result models since no fields wille be removed
# pydantic validates all overrides at runtime
# pyright: reportIncompatibleVariableOverride=false


from pydantic import Field

from compiler.models.SubjectModel import StreamId, StreamModel

from .CleanedResultModel import (
    CleanedPrimarySubjectModel,
    CleanedSchoolResultModel,
    CleanedStudentResultModel,
    StudentSubjectsModel,
)
from .Units import NonZeroFloat, NonZeroInt


class CompiledPrimarySubjectModel(CleanedPrimarySubjectModel):
    percentage: NonZeroFloat
    percentile_all_streams: NonZeroFloat
    rank_same_stream: NonZeroInt
    rank_all_streams: NonZeroInt


class CompiledStudentSubjectsModel(StudentSubjectsModel[CompiledPrimarySubjectModel]):
    pass


class CompiledStudentResultModel(CleanedStudentResultModel):
    primary_subjects: CompiledStudentSubjectsModel = Field()

    percentage: NonZeroFloat
    percentile_same_stream: NonZeroFloat
    percentile_all_streams: NonZeroFloat
    rank_same_stream: NonZeroInt
    rank_all_streams: NonZeroInt


class CompliedStreamModel(StreamModel):
    student_count: NonZeroInt


class CompiledSchoolResultModel(CleanedSchoolResultModel):
    # NOTE: calculate this after compiling student's results
    percentage_mean: NonZeroFloat
    percentage_median: NonZeroFloat
    percentage_max: NonZeroFloat
    percentage_min: NonZeroFloat

    streams: dict[StreamId, CompliedStreamModel]
    students: list[CompiledStudentResultModel]
