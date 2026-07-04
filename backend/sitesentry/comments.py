"""Render the audit comment deterministically from a template.

Form: "observation of hazard leading to outcome, with priority sentiment". The priority sentiment
is selected from the confirmed band, never invented. A language model may later smooth wording, but
the substance and the sentiment are fixed here.
"""
from __future__ import annotations

from .knowledge_base import KnowledgeBase
from .models import Finding, PriorityBand

_SENTIMENT = {
    PriorityBand.high: ", and requires prompt corrective action.",
    PriorityBand.medium: ", and should be addressed.",
    PriorityBand.low: ", and should be monitored.",
}


def render_comment(finding: Finding, kb: KnowledgeBase) -> str:
    template = None
    for aid in finding.applicable_actions:
        template = kb.actions[aid].comment_template or template
        if template:
            break
    if not template:
        template = "{who} observed without {control}{priority_sentiment}"
    control_label = finding.tags[0].split(".")[-1] if finding.tags else "a required control"
    return template.format(
        who=finding.who,
        control=control_label + " protection",
        hazard_context=finding.hazard_context,
        outcome=finding.outcome,
        priority_sentiment=_SENTIMENT[finding.priority],
    )
