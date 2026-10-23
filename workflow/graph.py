
from langgraph.graph import StateGraph, START, END

from workflow.state import QAState
from agents.requirement_agent import analyze_requirements
from agents.test_case_agent import generate_test_cases
from agents.risk_agent import analyze_risks
from agents.reviewer_agent import review_test_cases
from agents.automation_agent import generate_automation


def requirement_node(state: QAState) -> dict:
    print("\n[Agent 1] Analyzing requirements...")

    analysis = analyze_requirements(
        state["user_story"]
    )

    return {"requirement_analysis": analysis}


def test_case_node(state: QAState) -> dict:
    print("\n[Agent 2] Generating test cases...")

    cases = generate_test_cases(
        
        user_story=state["user_story"],
        requirement_analysis=state["requirement_analysis"],
        review_feedback=state.get("review_feedback", []),
        previous_test_cases=state.get("test_cases", ""),
    )

    return {
        "test_cases": cases,
        "revision_count": state.get("revision_count", 0) + 1
    }


def risk_node(state: QAState) -> dict:
    print("\n[Agent 3] Analyzing risks...")
    report = analyze_risks(
        user_story=state["user_story"],
        test_cases=state["test_cases"]
    )

    return {"risk_report": report.model_dump()}

def reviewer_node(state: QAState) -> dict:
    print("\n[Agent 4] Reviewing QA output...")

    review = review_test_cases(
        user_story=state["user_story"],
        requirement_analysis=state["requirement_analysis"],
        test_cases=state["test_cases"],
        risk_report=state["risk_report"]
    )

    return {
        "review_result": review.model_dump(),
        "review_feedback": (
            review.issues + review.recommendations
        )
    }




def route_review(state: QAState) -> str:
    review = state["review_result"]

    score = review.get("score", 0)
    decision = review.get("decision", "REVISE")
    attempts = state.get("revision_count", 0)

    issues = review.get("issues", [])
    recommendations = review.get("recommendations", [])

    print(f"\n[Reviewer] Decision: {decision}")
    print(f"[Reviewer] Score: {score}/100")

    if issues:
        print("\n[Reviewer] Issues:")
        for issue in issues:
            print(f"  - {issue}")

    if recommendations:
        print("\n[Reviewer] Recommendations:")
        for recommendation in recommendations:
            print(f"  - {recommendation}")

    if decision == "APPROVED" and score >= 85:
        print("\nQA APPROVED")
        return "approved"

    if attempts >= 2:
        print("\nQA REVIEW STOPPED: Maximum attempts reached.")
        return "max_revisions"

    print("\nQA REVISION REQUIRED")
    return "revise"





def automation_node(state: QAState) -> dict:
    print("\nGenerating Playwright automation...")

    result = generate_automation(
        user_story=state["user_story"],
        test_cases=state["test_cases"]
    )

    return {
        "automation_result": result.model_dump()
    }


def build_qa_graph():
    builder = StateGraph(QAState)

    builder.add_node(
        "requirement_agent",
        requirement_node
    )

    builder.add_node(
        "test_case_agent",
        test_case_node
    )

    builder.add_edge(
        START,
        "requirement_agent"
    )

    builder.add_edge(
        "requirement_agent",
        "test_case_agent"
    )

    builder.add_edge(
        "test_case_agent",
        "risk_agent"
    )

    builder.add_node(
        "risk_agent", 
        risk_node
    )

    builder.add_node(
        "reviewer_agent", 
        reviewer_node
    )

    builder.add_edge(
        "risk_agent", 
        "reviewer_agent"
    )

    builder.add_node (
        "automation_agent", 
        automation_node
    )

    
    builder.add_conditional_edges(
        "reviewer_agent",
        route_review,
        {
            "approved": "automation_agent",
            "revise": "test_case_agent",
            "max_revisions": END,
        },
    )

    # Finish the workflow after Agent 5
    builder.add_edge(
        "automation_agent",
        END
    )

    return builder.compile()

