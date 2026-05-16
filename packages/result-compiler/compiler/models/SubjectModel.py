from pydantic import BaseModel, UUID4

SubjectId = int


class SubjectModel(BaseModel):
    """
    represents an indivisual subject
    """

    subject_id: SubjectId
    subject_name: str


class Streams(BaseModel):
    """
    represents an stream
    """

    stream_id: UUID4
    stream_name: str

    # subjects contained in this stream
    subjects: list[SubjectId]
