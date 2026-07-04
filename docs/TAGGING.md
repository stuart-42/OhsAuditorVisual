# TAGGING.md — tags, reason codes & the NLP suggestion loop

## Three inputs per finding

1. **Tags** — hierarchical, multi-label, controlled vocabulary (from the pack taxonomy).
   The structured source of truth.
2. **Reason codes** — controlled vocabulary for *why* the control failed. Second dimension
   that drives regulatory routing (see `DATA_MODEL.md`, keyed on `(tag × reason)`).
3. **Description** — free-text. Enrichment + NLP training data. Never the primary key.

Why all three: tags alone can't express causation, and causation changes the regulation
engaged. Free-text alone is unusable as training labels. Controlled-but-with-free-text is
the balance.

## The NLP tag-suggestion loop

Goal: as the inspector types a description, the app proposes tags (and candidate reason
codes) from the controlled vocabulary; the human confirms/amends (HITL).

- **Model:** a small multi-label text classifier — DistilBERT / ModernBERT class. Runs cheap,
  can later go on-device.
- **Labels:** `(description → human-confirmed tags)` pairs. Every confirmation in the app is
  a clean label. This is the same flywheel as the vision tagger — both *propose* into the same
  vocabulary; the human *disposes*.
- **Symmetry:** text-suggester (Phase 1) and vision-suggester (Phase 2) share the vocabulary
  and the HITL confirmation path, so they reinforce each other's training data.

## Cold start (no labels yet)

1. **Rules/keywords first** — seed with keyword→tag rules ("no helmet", "hard hat" → `ppe.head`)
   so the app is useful on day one and starts gathering confirmations.
2. **Zero-shot bridge** — optionally use an LLM (or zero-shot classifier) to propose tags from
   free-text early, with the human confirming. Cheap, no training needed.
3. **Train when ripe** — once enough confirmed pairs exist (low thousands across tags), fine-tune
   the small classifier and retire the zero-shot bridge for the common cases.
4. **Active learning** — prioritise low-confidence / corrected items for review; they're the most
   informative labels.

## Guardrails

- Suggestions are **advisory + HITL** — never auto-applied.
- **Vocabulary leads, text assists** — don't let free-text become the key, or label noise
  wrecks the training set.
- **Free-text is a PII surface** — UI hint not to name individuals; redact descriptions before
  any text enters a training set (see `gdpr-dpia`).
