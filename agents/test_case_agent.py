
import os
from utils.gemini_client import generate_with_retry
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_test_cases(
    user_story: str,
    requirement_analysis: str,
    review_feedback: list[str] | None = None,
    previous_test_cases: str = "",
) -> str:
    """
    Generate or revise QA test cases using Gemini.

    Initial generation:
        Uses the user story and requirement analysis.

    Revision:
        Uses the previous test suite and reviewer
        feedback to produce a complete improved suite.
    """

    if not user_story.strip():
        raise ValueError("User story cannot be empty")

    if not requirement_analysis.strip():
        raise ValueError(
            "Requirement analysis cannot be empty"
        )

    feedback_items = review_feedback or []

    if feedback_items:
        feedback_section = "\n".join(
            f"{index}. {item}"
            for index, item in enumerate(
                feedback_items, start=1
            )
        )

        revision_instructions = f"""
        THIS IS A TEST CASE REVISION.

        PREVIOUS TEST CASES:
        {previous_test_cases or "Not provided"}

        REVIEWER FEEDBACK:
        {feedback_section}

        REVISION RULES:

        1. Address every reviewer issue and recommendation.

        2. Preserve valid existing test cases.

        3. Preserve existing test case IDs whenever possible.

        4. Add new test cases for missing coverage.

        5. Do not limit the number of test cases.

        6. Correct priority inconsistencies.

        7. Add missing positive, negative, boundary,
           security, integration, and error scenarios.

        8. Clearly mark unspecified requirements as
           "Pending clarification".

        9. Do not invent product behavior or business rules.

        10. Return the COMPLETE revised test suite.

        11. Include a "Reviewer Feedback Addressed"
            section mapping each issue to its correction.

        12. If a reviewer recommendation depends on an
            unconfirmed feature, identify the test as
            conditional rather than assuming the
            feature exists.
        """

    else:
        revision_instructions = """
        THIS IS INITIAL TEST CASE GENERATION.

        Generate comprehensive test cases covering:

        - Positive functionality
        - Negative functionality
        - Boundary conditions
        - Security
        - Error handling
        - Important edge cases

        Start with approximately 12 test cases,
        but add more when necessary for coverage.

        Clearly identify missing business requirements.
        """

    prompt = f"""
    You are a Senior QA Test Design Engineer.

    Your responsibility is to create comprehensive,
    traceable, risk-aware test cases.

    ORIGINAL USER STORY:
    {user_story}

    REQUIREMENT ANALYSIS FROM AGENT 1:
    {requirement_analysis}

    {revision_instructions}

    TEST CASE FORMAT:

    For every test case include:

    - Test Case ID
    - Title
    - Priority (P0/P1/P2)
    - Preconditions
    - Test Steps
    - Expected Result
    - Test Type
    - Requirement Status

    QUALITY RULES:

    - Use unique test case IDs.
    - Provide clear and testable expected results.
    - Cover high-risk functionality thoroughly.
    - Keep priorities consistent with business impact
      and the risks identified in the requirements.
    - Do not invent missing requirements.
    - Do not claim that an unconfirmed feature exists.
    - Identify tests blocked by missing requirements.
    - Do not delete valid existing coverage during revision.
    - Return the entire test suite, not just changes.

    OUTPUT:
    Return readable Markdown test cases.
    """

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    try:
        response =generate_with_retry(
           client=client,
            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            ),
            contents=prompt,
        )

        if not response.text or not response.text.strip():
            raise RuntimeError(
                "Model returned no test cases"
            )

        return response.text.strip()

    finally:
        client.close()
