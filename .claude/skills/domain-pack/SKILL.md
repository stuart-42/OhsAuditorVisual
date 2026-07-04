---
name: domain-pack
description: The structure and interface contract for a swappable vertical "domain pack" so the same core engine can serve construction today and catering/food-safety, care homes, warehousing, or retail later. Use this skill whenever the work involves adding or editing a vertical, generalising the app beyond construction, defining the hazard taxonomy/regulation KB/report template structure, keeping domain knowledge out of the core engine, or planning the multi-domain roadmap. Trigger it even if the user only mentions "another sector", "catering", "reuse", "new vertical", or "generalise", and even if they don't name this skill.
---

# Domain Pack

The commercial thesis is **one engine, many verticals**. The core engine must stay
domain-agnostic; everything domain-specific lives in a pack that can be swapped or sold as an
add-on.

## A pack contains

```
packs/<vertical>/
├── pack.json            # id, name, version, regulatory jurisdiction
├── taxonomy.json        # hazard classes (see uk-construction-regs for the field shape)
├── regulations/         # clause text/summaries the reasoning model cites
├── corrective_actions/  # reusable action templates keyed by hazard
├── severity_rubric.json # how severity is scored for this vertical
├── detector/            # on-device model reference/weights (or pointer)
└── report_template/     # output template for this vertical
```

## Interface contract (what the core engine expects)

The engine only ever calls a pack through this contract — it never reads domain logic
directly:

- `getTaxonomy()` → hazard classes
- `detect(frame)` → candidate detections with confidence (edge model)
- `reason(reviewedFrame)` → regulation refs + draft corrective action (cloud/Bedrock)
- `severityFor(detection)` → severity score
- `renderReport(observations)` → report in the vertical's template

## Adding a new vertical (e.g. catering)

1. Copy `packs/construction/` to `packs/catering/`.
2. Replace taxonomy (food hygiene/H&S hazards), regulations (e.g. Food Safety Act 1990, Food
   Hygiene Regs 2013), corrective actions, severity rubric, detector weights, report template.
3. No core-engine changes should be required. If they are, the abstraction has leaked — fix
   the engine, not the pack.

Keep this contract stable. Resist the urge to special-case construction inside the engine.
