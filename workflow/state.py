
from typing import TypedDict


class QAState(TypedDict):
    user_story: str
    requirement_analysis: str
    test_cases: str
    risk_report: dict
    review_result: dict
    revision_count: int
    review_feedback: list[str]
    automation_result: dict