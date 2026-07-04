# Vision prototype (no AWS, no cost)

Validates the visual detection pipeline locally before any cloud is involved.

## Run it

```bash
cd prototype/vision_test
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# drop a few construction photos into sample_images/  (use consented/synthetic images)
python detect.py --images sample_images --out outputs
```

You'll get `outputs/annotated_*.jpg` (boxes drawn on) and `outputs/observations.json`
(shaped like the real Observation model).

## Cost / scope notes

- **£0** — runs on CPU, downloads a ~6MB model once, no API calls, no AWS.
- The class→hazard map in `detect.py` (`HAZARD_MAP`) is a **stub** to prove the seam.
  Swapping in a PPE/hazard-finetuned model later changes only the weights + map, not
  the interface — that interface is the domain-pack `detect()` contract.
- Keep **real** site imagery out of git (`.gitignore` already excludes `sample_media/`
  and video). Prefer synthetic or consented test images.

## Testing on GitHub instead of your laptop

The `vision-test` workflow (`.github/workflows/vision-test.yml`) runs this on GitHub's
free runners on demand and uploads the annotated images as an artifact you can download.
Trigger it from the Actions tab (Run workflow). Still no AWS.
