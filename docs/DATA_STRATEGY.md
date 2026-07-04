# DATA_STRATEGY.md — training data (range · source · number)

Phase 2 concern (vision). The audit-first build (Phase 1) is what *generates* this data, so
this strategy and the product reinforce each other.

## Number (per hazard class)

- Demo/pipeline: ~100–300 labelled images.
- Decent prototype: ~500–1,000.
- Production target: Ultralytics guidance ≥1,500 images **and** ≥10,000 instances per class
  (whole dataset incl. val/test).

Notes: **instances, not images, are the currency** — crowded site photos hit instance counts
fast. Freezing the backbone (head-only fine-tune) lowers the data/compute floor; full
fine-tune needs more but raises the ceiling. Augmentation (mosaic, mixup) multiplies for free.

## Source (best-to-worst on effort vs fit)

1. **Public datasets** — fastest start. **SH17** (~8,099 images, ~76k instances, 17 classes,
   de-biased, open for commercial use) is the anchor; plus Pictor-PPE, Roboflow "Construction
   Site Safety", ACID (machinery → plant–pedestrian), CPPE-5 (medical PPE). **Check each
   dataset licence individually** (dataset licence ≠ model-code licence; some are research-only).
2. **Own site capture** — best fit, worst GDPR exposure. Needs lawful basis + consent before
   images enter a training set. Tension: you can't blur a head to anonymise and still learn
   "hard hat on head" — training-data governance is stricter than inference-time redaction.
3. **Synthetic** — for scenes you can't safely stage (person at an unguarded edge). Fills the
   long tail; watch the sim-to-real gap.
4. **Web scraping** — noisy, licensing minefield. Avoid for commercial use.
5. **HITL label flywheel (the strategic one)** — every accept/amend in the app is a free,
   in-distribution label. Combine with open-vocab auto-labelling (YOLO-World / Grounding DINO)
   pre-fill + human correction = active learning. This is why audit-first is also data-first.

## Range (diversity — decides real-world vs demo)

Must span times of day, seasons, weather, lighting, angles, cameras. Out-of-distribution drop
is real (a YOLOv9-e PPE model fell to ~59% mAP cross-domain). Watch:
- **Safety paradox / imbalance** — the most important hazards are rarest and unstageable;
  synthesise + active-learn the tail.
- **Demographic & kit variety** — body types, skin tones, helmet colours, hi-vis styles,
  occlusion. Gaps here become blind spots. Copy SH17's deliberate de-biasing.

## Staged plan (fits the domain-pack design)

Public base (SH17 + machinery) → frozen-backbone fine-tune → augment → per-tenant top-up with
consented site images → HITL flywheel + synthetic tail. Each new vertical repeats step one
with its own dataset.
