import pandas as pd
from pydantic import UUID4, BaseModel, RootModel

SubjectId = str
StreamId = UUID4


class SubjectModel(BaseModel):
    """
    represents an indivisual subject
    """

    subject_id: SubjectId
    subject_name: str


def convert_subjects_to_series(subjects: list[SubjectId]) -> pd.Series:
    return pd.Series(subjects)


class StreamModel(BaseModel):
    """
    represents an stream
    """

    stream_id: StreamId

    # So stream name becomes primary_stream + secondary_stream
    # PCM, PCB, Commerce etc
    primary_stream: str

    # IP, MMS, Geo etc
    secondary_stream: str

    # subjects contained in this stream
    subjects: list[SubjectId]

    @property
    def subjects_series(self) -> pd.Series[SubjectId]:
        ser = pd.Series(self.subjects)
        return ser[ser != ""].sort_values().reset_index(drop=True)


# StreamJsonModel = RootModel[list[StreamModel]]
class StreamJsonModel(RootModel[list[StreamModel]]):
    def __getitem__(self, index: int) -> StreamModel | None:
        return self.root[index]

    def __len__(self) -> int:
        return len(self.root)
