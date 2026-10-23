
import os
from typing import Literal
from utils.gemini_client import generate_with_retry
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


class ReviewResult(BaseModel):
    decision: Literal["APPROVED", "REVISE"]
    score: int = Field(ge=0, le=100)
    issues: list[str]
    recommendations: list[str]


def review_test_cases(
    user_story: str,
    requirement_analysis: str,
    test_cases: str,
    risk_report: dict
) -> ReviewResult:

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    prompt = f"""
    You are an independent Senior QA Reviewer.

    ORIGINAL USER STORY:
    {user_story}

    REQUIREMENT ANALYSIS:
    {requirement_analysis}

    TEST CASES:
    {test_cases}

    RISK REPORT:
    {risk_report}

    Evaluate:
    1. Requirement coverage
    2. Positive and negative scenarios
    3. Boundary conditions
    4. Security test coverage
    5. Clarity of expected results
    6. Unsupported assumptions
    7. Risk and priority consistency

    Give a score from 0 to 100.

    APPROVED: score >= 85 and no critical issues.
    REVISE: otherwise.

    Mark unconfirmed requirements clearly.
    Do not claim potential vulnerabilities are
    confirmed defects.
    """

    try:
        response = generate_with_retry(
            client=client,
            model=os.getenv(
                "GEMINI_MODEL", "gemini-2.5-flash"
            ),
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": ReviewResult.model_json_schema()
            }
        )

        if not response.text:
            raise RuntimeError("Reviewer returned no output")

        return ReviewResult.model_validate_json(
            response.text
        )
    finally:
        client.close()
