import json
import sys

from .agents import NaiveAgent, NotesAgent, CarefulAgent
from .runner import SCENARIOS, run

POLICIES = (NaiveAgent, NotesAgent, CarefulAgent)
COLS = ["scenario", "agent", "status", "claim", "target_claim_match", "scenario_pass", "evidence_ok",
        "duplicate_actions", "missed_actions", "unexpected_actions",
        "unauthorized_attempts", "denied_attempts", "invalid_action_attempts", "unsupported_success"]


def build_rows():
    return [run(p, s) for s in SCENARIOS for p in POLICIES]


def main(argv):
    rows = build_rows()
    print(" | ".join(COLS))
    for r in rows:
        print(" | ".join(str(r[c]) for c in COLS))
    if len(argv) > 1:
        with open(argv[1], "w") as f:
            json.dump(rows, f, indent=2)


if __name__ == "__main__":
    main(sys.argv)
