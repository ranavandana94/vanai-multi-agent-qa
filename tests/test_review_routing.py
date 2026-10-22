
from workflow.graph import route_review


def test_approved_review():
    state = {
        "review_result": {
            "decision": "APPROVED",
            "score": 90
        },
        "revision_count": 1
    }

    assert route_review(state) == "approved"


def test_low_score_requires_revision():
    state = {
        "review_result": {
            "decision": "APPROVED",
            "score": 70
        },
        "revision_count": 1
    }

    assert route_review(state) == "revise"


def test_maximum_attempts():
    state = {
        "review_result": {
            "decision": "REVISE",
            "score": 65
        },
        "revision_count": 2
    }

    assert route_review(state) == "max_revisions"
