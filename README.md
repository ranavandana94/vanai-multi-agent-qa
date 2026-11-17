# VANAI Multi-Agent QA Studio

An AI-powered, multi-agent Quality Engineering framework built with **Python, LangGraph, Google Gemini, Pydantic, and Playwright**.

The project demonstrates how specialized AI agents collaborate to analyze software requirements, generate test cases, evaluate testing risks, review QA deliverables, and draft Playwright automation for approved coverage.

## Features

- **Requirement Analysis Agent:** Identifies functional requirements, acceptance criteria, missing requirements, and edge cases.
- **Test Case Generation Agent:** Generates positive, negative, boundary, and security test scenarios. Review feedback is passed back into later attempts.
- **Risk Analysis Agent:** Evaluates test risks and recommends execution priorities.
- **QA Reviewer Agent:** Reviews test coverage, identifies gaps, and recommends improvements.
- **Agentic Review Loop:** Approves the QA output only when the decision is `APPROVED` and the score is at least 85. Otherwise it requests a revision, up to a maximum of two attempts.
- **Playwright Automation Agent:** After QA approval, converts the approved test cases into pytest-Playwright code. The draft is syntax-checked without being executed.
- **Automation Code Reviewer:** Performs a static review of the generated code. It does not run the tests, and its `execution_status` stays `NOT_RUN`.
- **Checkpoint Resume:** Each run is saved in a SQLite checkpoint so a stopped workflow can be resumed with the same thread ID.
- **Structured Outputs:** Uses Pydantic to validate risk, review, automation, and automation-review reports.

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
    +---- MAX ATTEMPTS ------------> End
    |
    +---- APPROVED (score >= 85)
    |
    v
Playwright Automation Agent
    |
    v
Automation Code Reviewer
    |
    v
Final QA Report
```

Approved runs save two files under `generated_tests/drafts/`:

- `automation_<id>.py.txt` — generated Playwright code. The `.py.txt` extension keeps pytest from collecting the draft.
- `automation_<id>.json` — syntax validation report. `execution_status` is `not_run` and `review_status` is `pending` at save time.

A syntax error is written into the report and stops the automation step. The original draft is still kept.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core development |
| LangGraph | Agent orchestration and shared state |
| LangGraph SQLite checkpointer | Resume a workflow by thread ID |
| Google Gemini | LLM-powered analysis and code generation |
| Pydantic | Structured data validation |
| Playwright | Browser automation target for generated tests |
| Pytest | Routing tests and Playwright setup check |

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

Install the Playwright browser used by the setup test:

```bash
playwright install
```

Create a `.env` file:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

## Run the application

`--thread-id` is required. Use a new ID for each fresh run:

```bash
python main.py --thread-id password-reset-001
```

If that run stops, resume the saved checkpoint:

```bash
python main.py --thread-id password-reset-001 --resume
```

A thread ID that already has a checkpoint cannot be started again. Choose a new `--thread-id`, or pass `--resume`. Checkpoints are stored in `.checkpoints/qa.sqlite`, which is ignored by git.

`main.py` starts from this built-in user story:

> As a registered user, I want to reset my password using my email so that I can regain access to my account.

The printed report includes requirement analysis, test cases, the risk report, the QA review, the automation result, and the automation code review.

*AI-generated assessments and test scripts are advisory and require human verification before execution.*

## Testing

Run the workflow routing tests:

```bash
python -m pytest tests/test_review_routing.py -v
```

Run the Playwright browser setup check:

```bash
python -m pytest tests/test_playwright_setup.py -v
```

Run every test under `tests/`:

```bash
python -m pytest tests/ -v
```

## Planned Enhancements

- Execute generated Playwright tests and analyze the results
- Route a failed automation review back to the automation agent
- Streamlit dashboard
- Test case export to JSON and CSV
- Improved deterministic quality checks
- CI/CD integration using GitHub Actions

## Project Goals

Demonstrate practical skills in Agentic AI, multi-agent orchestration, AI-assisted software testing, quality engineering, and LLM output evaluation.

## Security

API keys are stored in `.env` and must never be committed to version control. Generated Playwright drafts are syntax-checked only. Review them before running them, and do not point them at production accounts or data.

## Author

Vandana Chauhan

Quality Engineering | Test Automation | Agentic AI | AI Quality Engineering
