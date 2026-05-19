from pathlib import Path

from compiler.clean_results import clean_school_result
from compiler.models.RawResponseModels import RawSchoolResultJsonModel


def test_clean_school():
    sample_data = (Path(__file__).parent / "tmp_dav.json").read_text()
    raw = RawSchoolResultJsonModel.model_validate_json(sample_data)
    cleaned = clean_school_result(raw)

    (Path(__file__).parent.parent / ".notebooks/tmp_cleaned.json").write_text(
        cleaned.model_dump_json(indent=4)
    )
    assert cleaned
