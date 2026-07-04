"""Load the domain pack knowledge base and build the lookup indexes.

The knowledge is authored as legible structured files (see packs/construction/knowledge_base).
At load time those records are turned into keyed indexes for exact, deterministic recall. Nothing
here searches text; that is the separate retrieval assist added later.
"""
from __future__ import annotations

import json
from pathlib import Path

from .models import CanonicalAction, DutyScope, LegalStatus, Provision


class KnowledgeBase:
    def __init__(self, pack_dir: Path) -> None:
        self.pack_dir = Path(pack_dir)
        self.provisions: dict[str, Provision] = {}
        self.actions: dict[str, CanonicalAction] = {}
        # exact key: (tag, reason) -> {"provisions": [...], "actions": [...], "hazard": str}
        self.mapping: dict[tuple[str, str], dict] = {}
        self._load()

    def _read(self, name: str) -> dict:
        return json.loads((self.pack_dir / name).read_text())

    def _load(self) -> None:
        for p in self._read("provisions.json")["provisions"]:
            p = {**p, "legal_status": LegalStatus(p["legal_status"]), "duty_scope": DutyScope(p["duty_scope"])}
            self.provisions[p["id"]] = Provision(**p)
        for a in self._read("actions.json")["actions"]:
            self.actions[a["id"]] = CanonicalAction(**a)
        for row in self._read("mapping.json")["map"]:
            self.mapping[(row["tag"], row["reason"])] = {
                "provisions": row["provisions"],
                "actions": row["actions"],
                "hazard": row.get("hazard", ""),
            }

    def lookup(self, tag: str, reason: str) -> dict | None:
        """Exact keyed lookup — the deterministic spine. Returns None if the combination is unmapped."""
        return self.mapping.get((tag, reason))
