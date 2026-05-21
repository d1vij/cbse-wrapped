from pathlib import Path

from compiler.generate_results import generate_school_result
from compiler.models.CleanedResultModel import CleanedSchoolResultModel


def test_compile():
    # WARN: this might throw if this test runs before the test which generates the cleaned data
    cleaned = CleanedSchoolResultModel.model_validate_json(
        (Path(__file__).parent / "tmp_cleaned.json").read_text()
    )

    compiled = generate_school_result(cleaned)
    (Path(__file__).parent / "tmp_complied.json").write_text(
        compiled.model_dump_json(indent=4)
    )
    assert compiled
