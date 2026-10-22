from workflow.graph import build_qa_graph
import json

def main():
    user_story = """
    As a registered user,
    I want to reset my password using my email
    so that I can regain access to my account.
    """

    graph = build_qa_graph()

    initial_state = {
        "user_story": user_story,
        "requirement_analysis": "",
        "test_cases": "",
        "risk_report": {},
        "review_result": {},
        "revision_count": 0,
        "review_feedback": []      
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 50)
    print("REQUIREMENT ANALYSIS")
    print("=" * 50)
    print(result["requirement_analysis"])

    print("\n" + "=" * 50)
    print("GENERATED TEST CASES")
    print("=" * 50)
    print(result["test_cases"])
  

    print("\n" + "=" * 50)
    print("RISK ANALYSIS REPORT")
    print("=" * 50)

    print(json.dumps(result["risk_report"], indent=2))

    print("\n" + "=" * 50)
    print("QA REVIEW RESULT")
    print("=" * 50)

    print(json.dumps(result["review_result"], indent=2))

    print(
        f"\nTest case generation attempts: "
        f"{result['revision_count']}"
    ) 


if __name__ == "__main__":
    main()
