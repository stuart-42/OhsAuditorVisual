"""Standard-library self-check (no pytest needed). Mirrors tests/test_reasoning.py."""
from pathlib import Path

from sitesentry.consolidation import consolidate
from sitesentry.knowledge_base import KnowledgeBase
from sitesentry.models import Finding, PriorityBand
from sitesentry.reasoning import engage

PACK = Path(__file__).resolve().parents[1] / "packs" / "construction" / "knowledge_base"
kb = KnowledgeBase(PACK)


def head():
    return Finding(id="obs_001", hazard="head_injury", control_at_issue="ppe_head",
                   tags=["control.ppe.head"], reason_codes=["not_worn"], priority=PriorityBand.high)


def foot():
    return Finding(id="obs_002", hazard="foot_injury", control_at_issue="ppe_foot",
                   tags=["control.ppe.foot"], reason_codes=["not_worn"], priority=PriorityBand.medium)


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


print("Self-check:")
check("exact lookup hits", kb.lookup("control.ppe.head", "not_worn") is not None)
check("exact lookup misses cleanly", kb.lookup("control.ppe.head", "nope") is None)

f, unmapped = engage(head(), kb)
check("engage derives provisions", set(f.engaged_provisions) == {"ppe_reg4", "ppe_reg10", "mhswr_reg3", "hswa_s2", "ppe_reg7"})
check("no unmapped for known combo", unmapped == [])

res = consolidate([head(), foot()], kb)
reassess = [a for a in res.actions if a.action_id == "ca_reassess"]
check("shared action consolidated once", len(reassess) == 1)
check("shared action stems from both findings", set(reassess[0].from_findings) == {"obs_001", "obs_002"})

r1 = consolidate([head()], kb)
prov = next(a for a in r1.actions if a.action_id == "ca_provide_head").discharges_here
check("specific duties lead general", [p.duty_scope.value for p in prov] == sorted([p.duty_scope.value for p in prov], key=lambda s: 0 if s == "specific" else 1))

r1 = consolidate([head()], kb)
check("maintenance action closes ppe_reg7 gap", not any(g.provision.id == "ppe_reg7" for g in r1.gaps))
check("maintenance action appears in plan", any(a.action_id == "ca_maintain_ppe" for a in r1.actions))

_, un = engage(Finding(id="x", hazard="h", control_at_issue="c", tags=["control.ppe.hiviz"], reason_codes=["doesnt_fit"]), kb)
check("unmapped combination flagged", un == ["control.ppe.hiviz x doesnt_fit"])

print("\nAll self-checks passed.")
