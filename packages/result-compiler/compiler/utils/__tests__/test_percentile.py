from pathlib import Path

import pandas as pd

from compiler.models.CleanedResultModel import CleanedSchoolResultModel

from ..percentile import (
    calculate_percentile,
    get_score_percentile_matrix,
    get_score_matrix,
)


def test_percentile_calcuate():
    data = pd.Series(
        [ 80, 86, 94, 81, 76, 84, 81, 90, 92, 81, 89, 82, 73, 88, 89, 75, 76, 90, 77, 85, 84, 76, 94, 73, 74, 82, 86, 63, 84, 76, 85, 88, 74, 75, 90, 87, 76, 82, 76, 80, 88, 84, 89, 66, 77, 87, 86, 86, 87, 86, 79, 92, 85, 87, 81, 88, 84, 82, 86, 84, 90, 80, 88, 81, 90, 90, 75, 95, 85, 76, 85, 75, 92, 87, 92, 80, 74, 82, 82, 72, 75, 90, 87, 91, 73, 85, 66, 93, 82, 86, 85, 90, 69, 83, 88, 80, 99, 90, 87, 83, 91, 82, 85, 85, 86, 93, 84, 95, 82, 94, 89, 78, 90, 87, 84, 85, 96, 93, 86, 95, 92, 86, ]
    )  # fmt: skip

    assert calculate_percentile(1, data) == 0.0
    assert calculate_percentile(85, data) == 50.0  # since median of the dataset is 85
    assert (
        calculate_percentile(data.max(), data) < 100
    )  # since the percentile calculation is exclusive of our score


def test_score_matrix():
    students = CleanedSchoolResultModel.model_validate_json(
        (
            Path(__file__).parent.parent.parent / ".notebooks" / "tmp_cleaned.json"
        ).read_text()
    )
    assert get_score_matrix(students) is not None


def test_percentile_matrix():
    assert (
        get_score_percentile_matrix(
            CleanedSchoolResultModel.model_validate_json(
                (
                    Path(__file__).parent.parent.parent
                    / ".notebooks"
                    / "tmp_cleaned.json"
                ).read_text()
            )
        )
        is not None
    )
