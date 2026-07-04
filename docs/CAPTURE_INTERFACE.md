# CAPTURE_INTERFACE — on-site observation capture (Milestone One)

The single entry point for recording observations is the product on site. If capture is slow, the
tool fails regardless of the reasoning behind it. Speed and ease for an auditor in the field are a
fixed requirement, not a refinement.

## Layered design — each layer catches what the one above leaves out

1. **Sections are organisational, not exhaustive.** Pitch sections at the level a practitioner would
   structure an inspection — about a dozen themes under premises / practices / people, "protective
   equipment" being one. Thorough in coverage of themes, coarse in content. Sections stay short and
   stable.
2. **Prompted elements carry the common cases.** Within a section, list only the vital few worth
   actively prompting for (protective equipment: head, foot, eye, hand, hearing, respiratory,
   high-visibility). These drive one-tap capture and cover the large majority of entries. Not a
   complete enumeration.
3. **Type-ahead catches the long tail.** Anything not worth a standing prompt is reached by typing a
   few letters against the full controlled vocabulary. Depth lives in the vocabulary, not in the
   section layout — the auditor filters into it, never scrolls it.
4. **Unmapped-capture-and-triage catches the genuine gap.** A finding with no matching tag is
   recorded as free text, marked unmapped, and queued for triage; later the pack maintainer decides
   whether it warrants a new vocabulary entry. Prevents on-site dead ends and signals where the
   vocabulary needs extending.

## Capture mechanics

- **Context scopes the list.** The current section's prompted elements are the default shortlist —
  never the master taxonomy.
- **Prompted elements are tap targets.** Tapping an element and choosing an outcome is the
  observation: one tap for satisfactory, tap-then-reason for a finding. No searching, because the
  prompt pre-selected the tag.
- **Recents and frequency surface first.** The auditor's most-used or most-recent tags (overall and
  for this site) appear first; most auditors repeat the same findings, so this covers the bulk in
  one tap.
- **Camera-first option.** The entry point can be the camera: photograph, then the section-scoped
  tags appear. Sets up phase two cleanly, where the image pre-suggests the tag.

## Division of responsibility (the rule that makes it hold)
Sections and prompted elements are tuned for the common path; the controlled vocabulary is tuned for
completeness; type-ahead bridges them; unmapped-capture catches the rest. Effort goes into the
per-section prompted-element shortlist; depth accumulates in the vocabulary over time.

## Constraints carried from the rest of the design
The vocabulary the interface offers and the keys in the knowledge base come from one source, so an
auditor can never select a combination that has no entry. Every selection is a controlled value that
keys the deterministic lookup directly. Free text only assists (suggests a tag for the human to
confirm); it never keys the authoritative lookup. All capture remains human-in-the-loop and
advisory.
