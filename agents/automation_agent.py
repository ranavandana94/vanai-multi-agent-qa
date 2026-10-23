
import os
import ast
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel, Field

load_dotenv()


# --------------------------------------------------
# Structured output from the Automation Agent
# --------------------------------------------------

class AutomationResult(BaseModel):
    framework: str = Field(
        description="Automation framework used"
    )
    test_code: str = Field(
        description="Generated Python Playwright test code"
    )
    notes: list[str] = Field(
        description="Setup instructions, assumptions, and limitations"
    )


# --------------------------------------------------
# Agent 5: Playwright Automation Engineer
# --------------------------------------------------

def generate_automation(
    user_story: str,
    test_cases: str
) -> AutomationResult:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from the .env file"
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are a Senior QA Automation Engineer specializing
    in Python, pytest, and Playwright.

    Your responsibility is to convert approved manual
    test cases into maintainable Playwright automation.

    USER STORY:
    {user_story}

    APPROVED TEST CASES:
    {test_cases}

    AUTOMATION REQUIREMENTS:

    1. Use Python and pytest-playwright.

    2. Use the pytest-playwright page fixture.

    3. Prefer accessible Playwright locators:
       - get_by_role()
       - get_by_label()
       - get_by_placeholder()
       - get_by_test_id()

    4. Use Playwright expect() assertions.

    5. Cover important positive, negative, and
       boundary scenarios where practical.

    6. Do not hardcode passwords, API keys,
       authentication tokens, or other secrets.

    7. Read configuration and test credentials
       from environment variables.

    8. Do not invent real application URLs,
       selectors, or test credentials.

    9. When information is missing, use clearly
       marked placeholders and document them
       in the notes.

    10. Do not include destructive actions,
        payment submissions, or production
        data modifications.

    11. Generate valid Python code that can be
        saved into a pytest test file.

    12. Do not use arbitrary sleeps.
        Rely on Playwright's auto-waiting.

    13. Keep test functions independent.

    14. Clearly identify scenarios that cannot
        be automated without additional details.

    OUTPUT FORMAT:

    Return structured JSON containing:

    framework:
        "pytest-playwright"

    test_code:
        Complete Python automation code.

    notes:
        List of assumptions, missing details,
        environment setup, and limitations.
    """

    max_attempts = 3
    response = None

    try:
        # ------------------------------------------
        # Gemini API call with retry handling
        # ------------------------------------------

        for attempt in range(1, max_attempts + 1):

            try:
                print(
                    f"\n[Agent 5] Generating automation "
                    f"(attempt {attempt}/{max_attempts})..."
                )

                response = client.models.generate_content(
                    model=os.getenv(
                        "GEMINI_MODEL",
                        "gemini-2.5-flash"
                    ),
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": (
                            AutomationResult.model_json_schema()
                        ),
                    },
                )

                break

            except errors.ServerError as error:

                status_code = getattr(
                    error, "code", None
                )

                if status_code not in (
                    500, 502, 503, 504
                ):
                    raise

                if attempt == max_attempts:
                    raise RuntimeError(
                        "Gemini is temporarily unavailable "
                        "after 3 attempts. Please try again later."
                    ) from error

                wait_seconds = 2 ** attempt

                print(
                    f"[Agent 5] Gemini server error "
                    f"{status_code}. Retrying in "
                    f"{wait_seconds} seconds..."
                )

                time.sleep(wait_seconds)

        # ------------------------------------------
        # Validate response
        # ------------------------------------------

        if response is None or not response.text:
            raise RuntimeError(
                "Automation Agent returned an empty response."
            )

        result = AutomationResult.model_validate_json(
            response.text
        )

        # ------------------------------------------
        # Validate generated Python syntax
        # ------------------------------------------

        try:
            ast.parse(result.test_code)

        except SyntaxError as error:
            raise ValueError(
                "Automation Agent generated invalid "
                f"Python code: {error}"
            ) from error

        print(
            "\n[Agent 5] Playwright code generated "
            "and syntax validated successfully."
        )

        return result

    finally:
        client.close()
