import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from utils.gemini_client import generate_with_retry


load_dotenv()


class TestRisk(BaseModel):
    test_case_id: str
    risk_level: str
    reason: str
    recommended_priority: str


class RiskReport(BaseModel):
    overall_risk: str
    risks: list[TestRisk] = Field(default_factory=list)
    summary: str


def analyze_risks(
    user_story: str,
    test_cases: str
) -> RiskReport:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
    You are a Senior QA Risk Analysis Agent.

    USER STORY:
    {user_story}

    GENERATED TEST CASES:
    {test_cases}

    Analyze all test cases and identify:

    1. Risk level: High, Medium, Low
    2. Reason for the risk
    3. Recommended test priority: P0, P1, P2
    4. Overall feature risk
    5. Summary of major testing concerns

    Consider:
    - Security
    - Business impact
    - User impact
    - Likelihood of failure
    - Missing requirements

    Do not assume unconfirmed business rules.
    Preserve the original test case IDs.
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
                "response_json_schema": RiskReport.model_json_schema()
            }
        )

        if not response.text:
            raise RuntimeError("Risk Agent returned empty output")

        return RiskReport.model_validate_json(
            response.text
        )

    finally:
        client.close()
