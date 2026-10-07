import math

import pytest

from errors import ValidationError
from models import Assessment, parse_assessment, parse_mark, parse_number, parse_student


def test_numeric_string_accepted() -> None:
    assert parse_number("42.5", "score") == 42.5


def test_text_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number("text", "score")


def test_bool_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number(True, "score")


def test_nan_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_number(math.nan, "score")


def test_zero_total_rejected() -> None:
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Midterm",
            weight=30.0,
            total=0.0,
        )


def test_negative_score_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_mark(
            {
                "student": "S1",
                "assessment": "A1",
                "score": -1,
            }
        )


def test_missing_field_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student(
            {
                "id": "S1",
            }
        )


def test_payload_not_dict_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student(["S1", "Alice"])


def test_valid_assessment_parsed_correctly() -> None:
    assessment = parse_assessment(
        {
            "id": "A1",
            "title": "Midterm",
            "weight": "30",
            "total": "100",
        }
    )

    assert assessment == Assessment(
        id="A1",
        title="Midterm",
        weight=30.0,
        total=100.0,
    )