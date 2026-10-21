
from unittest.mock import patch

import pytest
from hypothesis import given, strategies as st

import gradebook



@given(
    scores=st.lists(
        st.integers(min_value=0, max_value=20),
        min_size=1,
        max_size=5,
    )
)
def test_percentage_does_not_exceed_assessment_weight(scores):
    state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"},
        },
        "assessments": {
            "A1": {
                "id": "A1",
                "title": "Quiz",
                "weight": 10,
                "total": 20,
            },
        },
        "marks": [],
    }

    with patch.object(gradebook, "STATE", state):
        with patch.object(gradebook, "save"):
            for score in scores:
                gradebook.add_mark({
                    "student": "S1",
                    "assessment": "A1",
                    "score": score,
                })

        assert float(gradebook.pct("S1")) <= 10
