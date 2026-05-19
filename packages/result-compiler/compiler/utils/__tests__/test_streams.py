import pandas as pd

from compiler.models.SubjectModel import StreamJsonModel
from compiler.utils.json_utils import read_from

from ..stream_utils import (
    get_stream_metadata,
    resolve_stream,
)


# TODO: Add before each test to load the streams
def test_streams_data_loading():
    streams = StreamJsonModel.model_validate_json(read_from("streams.json"))
    assert streams


def test_subject_codes_type():
    streams = StreamJsonModel.model_validate_json(read_from("streams.json"))
    first = streams[0]
    if first:
        assert isinstance(first.subjects_series, pd.Series)


def test_stream_resolution():
    subjects_series = pd.Series(["301", "041", "042", "043", "065"])
    stream_id = resolve_stream(subjects_series)

    assert stream_id is not None
    meta = get_stream_metadata(stream_id)
    assert meta is not None

    assert meta.primary_stream == "PCM"
    assert meta.secondary_stream == "IP"


def test_unknown_stream_resolution():
    subjects_series = pd.Series(["301", "041", "042", "043", "068"])
    stream_id = resolve_stream(subjects_series)

    assert stream_id is None
