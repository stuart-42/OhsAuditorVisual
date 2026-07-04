# MODEL_CHOICE.md — vision model selection & licence decision

Phase 2 concern (vision). Logged now so it isn't forgotten when we get there.

## Prototype model

`prototype/vision_test/` uses **YOLO11-nano** purely to prove the pipeline. It is trained on
COCO (person, truck…), **not** hazards — its detections are not safety signal. Treat it as
disposable; it must never enter the commercial codebase.

## Critical findings

1. **A generation behind for edge.** The current Ultralytics model is **YOLO26** (Jan 2026):
   NMS-free, edge-optimised, simpler export to TFLite/CoreML/ONNX, ~43% faster CPU inference
   than YOLO11-n. Better default if we stay in this family.
2. **AGPL-3.0 is a commercial blocker.** Ultralytics YOLO (v5/v8/v11/v12/YOLO26) is AGPL-3.0:
   using the code or **trained/fine-tuned weights** requires open-sourcing the **entire**
   project or buying an Enterprise Licence. Fine-tuning does **not** escape this.

## Decision (to confirm before any production fine-tune)

Decide the licence **before** fine-tuning, because custom weights inherit the base licence.
Options:
- **Permissive base (preferred for closed SaaS):** e.g. **RF-DETR** (Apache-2.0-positioned;
  verify) or RT-DETR — fine-tune freely, no AGPL obligation.
- **Ultralytics Enterprise Licence:** if YOLO26's edge performance is worth the fee.

The domain-pack `detect()` contract means this is a weights-and-licence swap, not a redesign,
so the final pick can wait until we test on real hazard imagery.

## Architecture note

Two-stage (cheap edge detector for offline flagging + cloud VLM for reg reasoning) is the
right shape. The edge model is the swappable component; the reasoning lives server-side.
