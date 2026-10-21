
import pytest

from errors import ValidationError
from models import Assessment
import gradebook


@pytest.mark.parametrize("weight", [0, 100])
def test_assessment_accepts_boundary_weights(weight):
    assessment = Assessment(
        id="A1",
        title="Boundary Test",
        weight=weight,
        total=20,
    )
    assert assessment.weight == weight


@pytest.mark.parametrize("weight", [-0.01, 100.01])
def test_assessment_rejects_out_of_range_weights(weight):
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Boundary Test",
            weight=weight,
            total=20,
        )


def test_assessment_accepts_small_positive_total():
    assessment = Assessment(
        id="A1",
        title="Boundary Test",
        weight=10,
        total=0.01,
    )
    assert assessment.total == 0.01


def test_assessment_rejects_zero_total():
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Boundary Test",
            weight=10,
            total=0,
        )


@pytest.mark.parametrize(
    ("score", "should_pass"),
    [
        (0, True),
        (20, True),
        (-0.01, False),
        (20.01, False),
    ],
)
def test_add_mark_score_boundaries(state, monkeypatch, score, should_pass):
    monkeypatch.setattr(gradebook, "STATE", state)
    monkeypatch.setattr(gradebook, "save", lambda: None)

    state["assessments"]["A1"]["total"] = 20
    payload = {
        "student": "S1",
        "assessment": "A1",
        "score": score,
    }

    if should_pass:
        gradebook.add_mark(payload)
        assert len(state["marks"]) == 1
        assert state["marks"][0]["score"] == score
    else:
        with pytest.raises(ValidationError):
            gradebook.add_mark(payload)
        assert state["marks"] == []
