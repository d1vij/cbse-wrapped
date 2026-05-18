from .CleanedResultModel import CleanedStudentResultModel, CleanedSchoolResultModel


# all models will extend their corresponding cleaned
# result models since no fields wille be removed


class CompiledStudentResultModel(CleanedStudentResultModel): ...


class CompiledSchoolResultModel(CleanedSchoolResultModel): ...
