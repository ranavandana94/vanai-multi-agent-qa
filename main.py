import argparse
import json
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from workflow.graph import build_qa_graph


def print_results(result):
    sections = [
        ("REQUIREMENT ANALYSIS", "requirement_analysis"),
        ("GENERATED TEST CASES", "test_cases"),
        ("RISK ANALYSIS REPORT", "risk_report"),
        ("QA REVIEW RESULT", "review_result"),
        ("AUTOMATION RESULT", "automation_result"),
        ("AUTOMATION CODE REVIEW", "automation_review"),
    ]

    for title, key in sections:
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)

        value = result.get(key, "Not generated")
        if isinstance(value, (dict, list)):
            print(json.dumps(value, indent=2))
        else:
            print(value)

    print(
        "\nTest case generation attempts: "
        f"{result.get('revision_count', 0)}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--thread-id",
        required=True,
        help="Unique ID for this workflow run.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume an existing run from its saved checkpoint.",
    )
    args = parser.parse_args()

    checkpoint_dir = Path(__file__).resolve().parent / ".checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    database_path = checkpoint_dir / "qa.sqlite"

    config = {
        "configurable": {
            "thread_id": args.thread_id,
        }
    }

    initial_state = {
        "user_story": """
        As a registered user,
        I want to reset my password using my email
        so that I can regain access to my account.
        """,
        "requirement_analysis": "",
        "test_cases": "",
        "risk_report": {},
        "review_result": {},
        "revision_count": 0,
        "review_feedback": [],
        "automation_result": {},
        "automation_review": {},
    }

    with SqliteSaver.from_conn_string(str(database_path)) as checkpointer:
        graph = build_qa_graph(checkpointer=checkpointer)
        snapshot = graph.get_state(config)
        has_checkpoint = snapshot.created_at is not None

        if args.resume:
            if not has_checkpoint:
                parser.error(
                    "No checkpoint found for this thread ID. "
                    "Start it without --resume first."
                )

            if not snapshot.next:
                print("This run has already finished.")
                print_results(snapshot.values)
                return

            print(f"Resuming thread: {args.thread_id}")
            print(f"Pending nodes: {', '.join(snapshot.next)}")
            workflow_input = None
        else:
            if has_checkpoint:
                parser.error(
                    "This thread ID already exists. Use --resume "
                    "or choose a new --thread-id."
                )

            print(f"Starting thread: {args.thread_id}")
            workflow_input = initial_state

        try:
            result = graph.invoke(workflow_input, config=config)
        except Exception:
            print(
                "\nWorkflow stopped. After resolving the error, "
                "resume using:\n"
                f"python main.py --thread-id {args.thread_id} --resume"
            )
            raise

        print_results(result)


if __name__ == "__main__":
    main()