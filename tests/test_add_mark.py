
import pytest

import gradebook


def test_add_mark_saves_a_valid_mark(loaded, monkeypatch):
    saved = []
    monkeypatch.setattr(gradebook, "save", lambda: saved.append(True))

    gradebook.add_mark(
        {
            "student": "S1",
            "assessment": "A1",
            "score": 15,
        }
    )

    assert len(loaded["marks"]) == 1
    assert loaded["marks"][0]["student"] == "S1"
    assert loaded["marks"][0]["assessment"] == "A1"
    assert loaded["marks"][0]["score"] == 15
    assert "at" in loaded["marks"][0]
    assert saved == [True]



def test_add_mark_rejects_unknown_student(loaded):
    with pytest.raises(gradebook.NotFoundError, match="Student not found."):
        gradebook.add_mark(
            {
                "student": "UNKNOWN",
                "assessment": "A1",
                "score": 15,
            }
        )

    assert loaded["marks"] == []



def test_add_mark_rejects_unknown_assessment(loaded):
    with pytest.raises(
        gradebook.NotFoundError,
        match="Assessment not found.",
    ):
        gradebook.add_mark(
            {
                "student": "S1",
                "assessment": "UNKNOWN",
                "score": 15,
            }
        )

    assert loaded["marks"] == []



def test_add_mark_rejects_score_above_total(loaded):
    with pytest.raises(
        gradebook.ValidationError,
        match="score must not be greater than assessment total.",
    ):
        gradebook.add_mark(
            {
                "student": "S1",
                "assessment": "A1",
                "score": 25,
            }
        )

    assert loaded["marks"] == []

    
def test_add_mark_calls_save_once(loaded, monkeypatch):
    calls = []
    monkeypatch.setattr(gradebook, "save", lambda: calls.append("saved"))

    gradebook.add_mark(
        {
            "student": "S1",
            "assessment": "A1",
            "score": 15,
        }
    )

    assert calls == ["saved"]

