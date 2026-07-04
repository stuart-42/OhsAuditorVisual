"""Consolidate corrective actions across an inspection.

One canonical action is shown once, accumulating every engaged provision it discharges, ordered
specific-duty-first then general. Any engaged provision not covered by a selected action is a gap.
Entirely deterministic and reproducible.
"""

from __future__ import annotations

from .knowledge_base import KnowledgeBase
from .models import ConsolidatedAction, ConsolidationResult, Gap
from .reasoning import engage


def _scope_rank(duty_scope) -> int:
    # specific duties lead, general duties follow
    return 0 if duty_scope.value == "specific" else 1


def consolidate(findings, kb: KnowledgeBase) -> ConsolidationResult:
    engaged_by_finding: dict[str, list[str]] = {}
    actions_by_finding: dict[str, list[str]] = {}
    all_engaged: set[str] = set()

    for f in findings:
        f, _ = engage(f, kb)
        engaged_by_finding[f.id] = f.engaged_provisions
        actions_by_finding[f.id] = f.applicable_actions
        all_engaged.update(f.engaged_provisions)

    # union of selected actions across the inspection, deduplicated by action id
    selected: dict[str, list[str]] = {}  # action_id -> finding ids that selected it
    for fid, aids in actions_by_finding.items():
        for aid in aids:
            selected.setdefault(aid, [])
            if fid not in selected[aid]:
                selected[aid].append(fid)

    covered: set[str] = set()
    consolidated: list[ConsolidatedAction] = []
    for aid, finding_ids in selected.items():
        action = kb.actions[aid]
        # engaged provisions that this action discharges, in this inspection
        here = [kb.provisions[pid] for pid in action.discharges if pid in all_engaged]
        here.sort(key=lambda p: _scope_rank(p.duty_scope))
        covered.update(p.id for p in here)
        consolidated.append(
            ConsolidatedAction(
                action_id=aid,
                label=action.label,
                discharges_here=here,
                from_findings=finding_ids,
                acop_derived=action.acop_derived,
            )
        )

    # gaps: engaged provisions with no selected action covering them
    gaps: list[Gap] = []
    for pid in sorted(all_engaged - covered):
        stems = [fid for fid, prov in engaged_by_finding.items() if pid in prov]
        gaps.append(Gap(provision=kb.provisions[pid], from_findings=stems))

    # deterministic ordering: Approved-Code-of-Practice-derived actions first, then by label
    consolidated.sort(key=lambda c: (not c.acop_derived, c.label))
    return ConsolidationResult(actions=consolidated, gaps=gaps)
