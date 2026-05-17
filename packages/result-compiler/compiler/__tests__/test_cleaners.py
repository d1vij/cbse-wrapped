from pathlib import Path

from compiler.clean_results import clean_school_result
from compiler.models.RawResponseModels import RawSchoolResultJsonModel
from compiler.notebooks.sample_data import sample_data


def test_clean_school():
    raw = RawSchoolResultJsonModel.model_validate_json(sample_data.read_text())
    cleaned = clean_school_result(raw)

    Path("tmp_school.json").write_text(cleaned.model_dump_json(indent=4))
    assert cleaned
