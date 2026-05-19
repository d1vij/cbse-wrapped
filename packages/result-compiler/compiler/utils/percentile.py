import pandas as pd

from compiler.models.CleanedResultModel import (
    CleanedSchoolResultModel,
)
from compiler.models.Units import NonZeroFloat, NonZeroInt


def calculate_rank(marks: NonZeroInt, marks_series: pd.Series[NonZeroInt]) -> int:
    students_above = marks_series.sort_values(ascending=True)[marks_series > marks].size
    return students_above + 1


def calculate_percentile(
    marks: NonZeroInt, marks_series: pd.Series[NonZeroInt]
) -> NonZeroFloat:
    """
    Fn to calculate the percentile for provided marks and a series marks of all students.

    The formula used is non inclusive for the student's marks, which means the percentile
    calculated refers to the students who scored below the student. This means student with the max marks
    wont have 100 percentile since he cannot "score more than himself"
    """
    if marks_series.hasnans:
        raise ValueError("marks_series cannot have nans in it")
    students_total = marks_series.size
    students_same = marks_series[marks_series == marks].size
    students_below = marks_series[marks_series < marks].size
    return ((students_below + 0.5 * students_same) / students_total) * 100


def get_score_matrix(school_results: CleanedSchoolResultModel) -> pd.DataFrame:
    """
    Returns a dataframe with indexes as student rollnumbers and columns being marks in a particular subject code.
    Presence of NaN values imply that that particular student doesnt have that particular subject
    Example:
        ```
                    301   041   042   043   044   029    835  065   030   054   055
        roll_number
        15623211      80  80.0  82.0  81.0  81.0   NaN    NaN  NaN   NaN   NaN   NaN
        15623212      86  97.0  96.0  99.0  95.0   NaN    NaN  NaN   NaN   NaN   NaN
        15623213      94   NaN  90.0  94.0  96.0  98.0    NaN  NaN   NaN   NaN   NaN
        15623214      81  84.0  90.0  87.0  79.0   NaN    NaN  NaN   NaN   NaN   NaN
        15623215      76  86.0  74.0  86.0  86.0   NaN    NaN  NaN   NaN   NaN   NaN
        ...          ...   ...   ...   ...   ...   ...    ...  ...   ...   ...   ...
        15623366      82   NaN   NaN   NaN   NaN   NaN    NaN  NaN  82.0  70.0  53.0
        15623367      86   NaN   NaN   NaN   NaN   NaN    NaN  NaN  94.0  83.0  93.0
        15623368      97   NaN   NaN   NaN   NaN   NaN    NaN  NaN  98.0  95.0  98.0
        15623369      92   NaN   NaN   NaN   NaN   NaN  100.0  NaN  97.0  92.0  83.0
        15623370      86   NaN   NaN   NaN   NaN   NaN   99.0  NaN  82.0  89.0  80.0
        ```
    """
    students = school_results.students

    records: list[dict[str, int | str]] = []
    for student in students:
        record: dict[str, int | str] = {}
        record["roll_number"] = student.roll_number
        subjects = student.primary_subjects.model_dump().values()
        for subject in subjects:
            if subject is None:
                continue
            record[subject["subject_id"]] = subject["marks_total"]

        records.append(record)

    return pd.DataFrame(records).set_index("roll_number").astype(float)


def get_score_percentile_matrix(
    school_results: CleanedSchoolResultModel, score_matrix: pd.DataFrame | None = None
) -> pd.DataFrame:
    """
    Returns a dataframe with indexes as student rollnumbers and columns being the percentile in a particular subject code.
    Presence of NaN values imply that that particular student doesnt have that particular subject
    Example:
        ```
                           301        041        042        043        044        029
        roll_number
        15623211     21.034483  48.969072  59.009009  58.108108  31.250000        NaN
        15623212     56.206897  97.422680  97.747748  99.549550  72.916667        NaN
        15623213     92.758621        NaN  79.729730  91.441441  87.500000  92.592593
        15623214     24.827586  59.278351  79.729730  71.621622  18.750000        NaN
        15623215     13.448276  65.979381  37.387387  68.918919  39.583333        NaN
        ...                ...        ...        ...        ...        ...        ...
        15623366     31.034483        NaN        NaN        NaN        NaN        NaN
        15623367     56.206897        NaN        NaN        NaN        NaN        NaN
        15623368     98.275862        NaN        NaN        NaN        NaN        NaN
        15623369     85.517241        NaN        NaN        NaN        NaN        NaN
        15623370     56.206897        NaN        NaN        NaN        NaN        NaN
        ```
    """

    if score_matrix is not None:
        data_matrix = score_matrix.copy(deep=True)
    else:
        data_matrix = get_score_matrix(school_results)

    for col in data_matrix.columns:
        subject_series = data_matrix[col].dropna()
        for roll_number, marks in subject_series.items():
            data_matrix.at[roll_number, col] = calculate_percentile(
                marks, subject_series
            )

    return data_matrix
