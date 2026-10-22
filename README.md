# VANAI Multi-Agent QA Studio

An AI-powered, multi-agent Quality Engineering framework built with **Python, LangGraph, Google Gemini, and Pydantic**.

The project demonstrates how specialized AI agents collaborate to analyze software requirements, generate test cases, evaluate testing risks, and review QA deliverables.

## Features

- **Requirement Analysis Agent:** Identifies functional requirements, acceptance criteria, missing requirements, and edge cases.
- **Test Case Generation Agent:** Generates positive, negative, boundary, and security test scenarios.
- **Risk Analysis Agent:** Evaluates test risks and recommends execution priorities.
- **QA Reviewer Agent:** Reviews test coverage, identifies gaps, and recommends improvements.
- **Agentic Review Loop:** Uses conditional routing to approve outputs or request revisions, with a maximum-attempt safeguard.
- **Structured Outputs:** Uses Pydantic to validate risk and review reports.

## Architecture

```text
User Story
    |
    v
Requirement Analysis Agent
    |
    v
Test Case Generation Agent <--------+
    |                               |
    v                               |
Risk Analysis Agent                 |
    |                               |
    v                               |
QA Reviewer Agent                   |
    |                               |
    +---- REVISE -------------------+
    |
    +---- APPROVED / LIMIT REACHED
    |
    v
Final QA Report
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core development |
| LangGraph | Agent orchestration and shared state |
| Google Gemini | LLM-powered analysis |
| Pydantic | Structured data validation |
| Pytest | Workflow and routing tests |

## Installation

Clone the repository:

```bash
git clone https://github.com/ranavandana94/vanai-multi-agent-qa.git
cd vanai-multi-agent-qa
```

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Run the application:

```bash
python main.py
```

## Example Use Case

**User Story:** As a registered user, I want to reset my password using my email so that I can regain access to my account.

The agents collaborate to produce requirement analysis, QA test cases, risk assessments, and review feedback.

In an initial demonstration, the reviewer returned a score of 90/100 and approved the generated output.

*AI-generated assessments are advisory and require human verification.*

## Testing

Run the available automated tests:

```bash
python -m pytest tests/ -v
```

## Planned Enhancements

- Playwright Automation Engineer Agent
- Test execution and result analysis
- Streamlit dashboard
- Test case export to JSON and CSV
- Improved deterministic quality checks
- CI/CD integration using GitHub Actions

## Project Goals

Demonstrate practical skills in Agentic AI, multi-agent orchestration, AI-assisted software testing, quality engineering, and LLM output evaluation.

## Security

API keys are stored in `.env` and must never be committed to version control. AI-generated test scripts should be reviewed before execution.

## Author

Vandana Chauhan

Quality Engineering | Test Automation | Agentic AI | AI Quality Engineering
