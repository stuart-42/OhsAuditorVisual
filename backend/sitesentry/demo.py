"""Runnable worked example: the head + foot protection findings from the design doc."""

from __future__ import annotations

from pathlib import Path

from .comments import render_comment
from .consolidation import consolidate
from .knowledge_base import KnowledgeBase
from .models import Finding, PriorityBand
from .reasoning import engage

PACK = Path(__file__).resolve().parents[2] / "packs" / "construction" / "knowledge_base"


def main() -> None:
    kb = KnowledgeBase(PACK)
    head = Finding(
        id="obs_001",
        hazard="head_injury_falling_object",
        control_at_issue="ppe_head",
        tags=["control.ppe.head"],
        reason_codes=["not_worn"],
        who="An operative",
        hazard_context="overhead work was taking place",
        outcome="serious head injury from a falling object",
        priority=PriorityBand.high,
    )
    foot = Finding(
        id="obs_002",
        hazard="foot_injury_falling_object",
        control_at_issue="ppe_foot",
        tags=["control.ppe.foot"],
        reason_codes=["not_worn"],
        who="An operative",
        hazard_context="materials were being handled",
        outcome="a crush or penetration foot injury",
        priority=PriorityBand.medium,
    )

    for f in (head, foot):
        engage(f, kb)
        print(f"\nAudit comment ({f.id}): {render_comment(f, kb)}")

    result = consolidate([head, foot], kb)
    print("\nConsolidated corrective-action plan:")
    for a in result.actions:
        cites = "; ".join(
            f"{p.instrument} {p.section} [{p.duty_scope.value}]" for p in a.discharges_here
        )
        flag = "  (Approved Code of Practice-derived)" if a.acop_derived else ""
        print(f"  - {a.label}{flag}")
        print(f"      discharges: {cites}")
        print(f"      from findings: {', '.join(a.from_findings)}")
    print(f"\nGaps: {'none' if not result.gaps else ''}")
    for g in result.gaps:
        print(f"  - uncovered: {g.provision.instrument} {g.provision.section}")


if __name__ == "__main__":
    main()
