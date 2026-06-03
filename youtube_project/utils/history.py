"""Persist analyzed video history to a JSON file."""

import json
import os
from datetime import datetime


class VideoHistory:
    def __init__(self, path: str | None = None):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path = path or os.path.join(base, "data", "history.json")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def _load(self) -> list:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self, items: list) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    def add(self, url: str, title: str, thumbnail: str = "") -> None:
        items = self._load()
        items = [i for i in items if i.get("url") != url]
        items.insert(
            0,
            {
                "url": url,
                "title": title,
                "thumbnail": thumbnail,
                "analyzed_at": datetime.now().isoformat(),
            },
        )
        self._save(items[:50])

    def get_all(self) -> list:
        return self._load()

    def clear(self) -> None:
        self._save([])
