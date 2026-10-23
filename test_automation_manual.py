from pathlib import Path
from agents.automation_agent import generate_automation

user_story = (
    "As a user, I want to log in "
    "so that I can access my account."
)

test_cases = """
TC-001: Verify login with valid credentials.
Expected: User is redirected to the dashboard.

TC-002: Verify login with invalid credentials.
Expected: An appropriate error message is displayed.

TC-003: Verify required email and password fields.
Expected: Validation errors are displayed.
"""

print("\nTesting Agent 5 independently...")

result = generate_automation(
    user_story=user_story,
    test_cases=test_cases
)

print("\nFramework:", result.framework)
print("\nGenerated Playwright Code:\n")
print(result.test_code)

print("\nAssumptions and Setup Notes:")
for note in result.notes:
    print("-", note)



# Save AI-generated automation for human review.
# Do not execute the generated script automatically.

output_dir = Path("generated_tests")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "test_login_generated.py"

output_file.write_text(
    result.test_code,
    encoding="utf-8"
)

print(f"\nGenerated script saved to: {output_file}")
print("Review the script before executing it.")
