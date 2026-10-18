
import pytest

import gradebook


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param({}, "0", id="no-marks"),
        pytest.param({"A1": 15}, "7.5", id="quiz-15-of-20"),
        pytest.param({"A1": 20}, "10.0", id="quiz-full-marks"),
        pytest.param({"A1": 0}, "0.0", id="quiz-zero-score"),
        pytest.param(
            {"A1": 15, "A2": 40},
            "31.5",
            id="two-assessments",
        ),
    ],
)
def test_percentage_for_scores(loaded, scores, expected):
    for assessment, score in scores.items():
        loaded["marks"].append(
            {
                "student": "S1",
                "assessment": assessment,
                "score": score,
            }
        )

    result = gradebook.pct("S1")

    assert result == expected


def test_mark_for_unknown_assessment_is_ignored(loaded):
    loaded["marks"].append(
        {"student": "S1", "assessment": "GHOST", "score": 15}
    )

    result = gradebook.pct("S1")

    assert result == "0"
