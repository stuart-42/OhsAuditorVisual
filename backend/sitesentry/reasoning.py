"""Engage provisions and gather applicable actions for a finding — deterministic, no language model."""
from __future__ import annotations

from .knowledge_base import KnowledgeBase
from .models import Finding


def engage(finding: Finding, kb: KnowledgeBase) -> tuple[Finding, list[str]]:
    """Populate a finding's engaged provisions and applicable actions from the (tag x reason) map.

    Returns the enriched finding and a list of unmapped (tag, reason) pairs, so an unmapped
    combination is surfaced as a gap rather than silently dropped.
    """
    provisions: list[str] = []
    actions: list[str] = []
    unmapped: list[str] = []
    for tag in finding.tags:
        for reason in finding.reason_codes:
            hit = kb.lookup(tag, reason)
            if hit is None:
                unmapped.append(f"{tag} x {reason}")
                continue
            for pid in hit["provisions"]:
                if pid not in provisions:
                    provisions.append(pid)
            for aid in hit["actions"]:
                if aid not in actions:
                    actions.append(aid)
    finding.engaged_provisions = provisions
    finding.applicable_actions = actions
    return finding, unmapped
