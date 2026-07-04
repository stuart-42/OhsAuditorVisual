"""
Local visual prototype — NO AWS, NO API KEYS, runs on CPU for free.

What it does
------------
1. Loads a small open object detector (YOLO11-nano, auto-downloaded once).
2. Runs it over every image in ./sample_images.
3. Maps raw detections to OUR hazard taxonomy (a deliberate STUB — see HAZARD_MAP).
4. Writes an annotated image + an observations.json that matches the shape of the
   Observation model (status 'flagged', advisory=True, source='edge').

Why a stub map?
---------------
Off-the-shelf YOLO knows COCO classes (person, truck...), not "missing hard hat".
This proves the *pipeline and the seam* end-to-end for free. Later you swap the
weights for a PPE/hazard-finetuned model — the interface below does not change.
That swap point IS the domain-pack `detect()` contract from CLAUDE.md.

Run
---
    pip install -r requirements.txt
    python detect.py --images sample_images --out outputs
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import uuid
from pathlib import Path

from ultralytics import YOLO

# --- STUB taxonomy map: raw detector class -> candidate hazard flag (advisory) ---
# Replace with a real PPE/hazard model + proper mapping. Keep the shape identical.
HAZARD_MAP = {
    "person": {
        "hazard_id": "presence_person",
        "note": "Person detected — check PPE, position relative to edges/plant.",
    },
    "truck": {
        "hazard_id": "plant_present",
        "note": "Plant/vehicle detected — check pedestrian segregation.",
    },
    "forklift": {
        "hazard_id": "plant_present",
        "note": "Plant detected — check exclusion zone.",
    },
}

TENANT_ID = "dev-tenant-0001"  # placeholder; real value comes from auth later


def to_observation(image_name: str, detections: list[dict]) -> dict:
    """Shape a result like the Observation model (see observation-lifecycle skill)."""
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    return {
        "id": str(uuid.uuid4()),
        "tenant_id": TENANT_ID,
        "media": [{"type": "photo", "source_file": image_name, "redacted": False}],
        "ai_detections": [
            {
                "hazard_id": d["hazard_id"],
                "raw_class": d["raw_class"],
                "confidence": round(d["confidence"], 3),
                "source": "edge",
                "model_version": "yolo11n",
                "advisory": True,
                "note": d["note"],
            }
            for d in detections
        ],
        "status": "flagged",  # AI may only set 'flagged'; a human reviews next
        "created_at": now,
        "audit_log": [{"event": "ai_flagged", "by": "vision_test", "at": now}],
    }


def run(images_dir: Path, out_dir: Path, conf: float) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    model = YOLO("yolo11n.pt")  # downloads ~6MB on first run

    image_paths = [
        p for p in sorted(images_dir.iterdir())
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    ]
    if not image_paths:
        print(f"No images found in {images_dir}. Add some .jpg/.png files and re-run.")
        return

    observations = []
    for path in image_paths:
        result = model(str(path), conf=conf, verbose=False)[0]
        names = result.names
        detections = []
        for box in result.boxes:
            raw_class = names[int(box.cls)]
            mapped = HAZARD_MAP.get(raw_class)
            if not mapped:
                continue  # ignore classes we don't map yet
            detections.append({
                "raw_class": raw_class,
                "confidence": float(box.conf),
                **mapped,
            })

        # Save annotated image for visual inspection.
        annotated = out_dir / f"annotated_{path.name}"
        result.save(filename=str(annotated))

        obs = to_observation(path.name, detections)
        observations.append(obs)
        print(f"{path.name}: {len(detections)} mapped detection(s) -> {annotated.name}")

    (out_dir / "observations.json").write_text(json.dumps(observations, indent=2))
    print(f"\nWrote {out_dir / 'observations.json'} and annotated images to {out_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local hazard-vision prototype (no AWS).")
    parser.add_argument("--images", default="sample_images", type=Path)
    parser.add_argument("--out", default="outputs", type=Path)
    parser.add_argument("--conf", default=0.35, type=float, help="confidence threshold")
    args = parser.parse_args()
    run(args.images, args.out, args.conf)
