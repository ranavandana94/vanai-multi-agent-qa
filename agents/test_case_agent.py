
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_test_cases(
    user_story: str,
    requirement_analysis: str,
    review_feedback: list[str] | None = None
) -> str:
    """
    Generate QA test cases using the original
    user story and Agent 1's analysis.
    """

    if not user_story.strip():
        raise ValueError("User story cannot be empty")

    if not requirement_analysis.strip():
        raise ValueError("Requirement analysis cannot be empty")

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )
    feedback_text = "\n".join(review_feedback or [])


    prompt = f"""
    You are a Senior QA Test Design Engineer.

    ORIGINAL USER STORY:
    {user_story}

    REQUIREMENT ANALYSIS FROM AGENT 1:
    {requirement_analysis}

    REVIEWER FEEDBACK:
    {feedback_text}

    Generate 12 comprehensive test cases.

    Include:
    - Positive scenarios
    - Negative scenarios
    - Boundary value tests
    - Security scenarios
    - Edge cases

    For each test case provide:

    Test Case ID
    Title
    Priority (P0/P1/P2)
    Preconditions
    Test Steps
    Expected Result
    Test Type
    Requirement Status

    IMPORTANT RULES:
    - Address all reviewer feedback.
    - Do not invent business rules.
    - Preserve valid scenarios.
    - Clearly mark scenarios requiring clarification.
    - Do not treat assumptions as confirmed requirements.
    - Use "Pending clarification" when the expected
      result depends on an unspecified business rule.
    - Ensure test cases are clear and executable
      once requirements are confirmed.
    """

    try:
        response = client.models.generate_content(
            model=os.getenv(
                "GEMINI_MODEL", "gemini-2.5-flash"
            ),
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Model returned no test cases")

        return response.text

    finally:
        client.close()
