from unittest.mock import Mock

import pytest

import gradebook
from errors import ConflictError, ValidationError
from models import Assessment


def test_add_assessment_stores_and_saves(state):
    save = Mock()
    assessment = Assessment(
        id="A3",
        title="Final",
        weight=20,
        total=100,
    )

    gradebook.add_assessment(state, assessment, save)

    assert state["assessments"]["A3"]["title"] == "Final"
    save.assert_called_once()


def test_add_assessment_rejects_weight_over_100(state):
    save = Mock()
    assessment = Assessment(
        id="A3",
        title="Final",
        weight=70,
        total=100,
    )

    with pytest.raises(ValidationError):
        gradebook.add_assessment(state, assessment, save)

    assert "A3" not in state["assessments"]
    save.assert_not_called()


def test_add_assessment_rejects_duplicate_id(state):
    save = Mock()
    assessment = Assessment(
        id="A1",
        title="Duplicate Quiz",
        weight=20,
        total=100,
    )

    with pytest.raises(ConflictError):
        gradebook.add_assessment(state, assessment, save)

    save.assert_not_called()


def test_failed_save_leaves_no_trace(state):
    def failing_save():
        raise OSError("disk full")

    assessment = Assessment("A3", "Final", 10.0, 50.0)
    with pytest.raises(OSError):
        gradebook.add_assessment(state, assessment, failing_save)

    assert "A3" not in state["assessments"]
