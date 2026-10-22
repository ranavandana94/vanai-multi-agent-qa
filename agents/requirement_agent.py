
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def analyze_requirements(user_story: str) -> str:
    """
    Analyze a user story and identify
    functional requirements, gaps, and QA risks.
    """
    if not user_story.strip():
        raise ValueError("User story cannot be empty")

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    prompt = f"""
    You are a Senior QA Requirement Analyst.

    Analyze this user story:

    {user_story}

    Return the following sections:

    1. Functional Requirements
    2. Acceptance Criteria
    3. Missing Requirements
    4. Negative Scenarios
    5. Boundary Conditions
    6. Questions for the Product Owner

    Rules:
    - Do not invent business requirements.
    - Clearly distinguish confirmed requirements
      from suggested acceptance criteria.
    - Identify ambiguous or missing details.
    - Keep the output structured and concise.
    """

    try:
        response = client.models.generate_content(
            model=os.getenv(
                "GEMINI_MODEL", "gemini-2.5-flash"
            ),
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Model returned no text")

        return response.text
    finally:
        client.close()
