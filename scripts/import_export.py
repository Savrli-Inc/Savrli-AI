"""
Utilities for exporting and importing conversation/resource data.
This is intentionally simple and file-system-backed; swap in DB or cloud storage as needed.
"""
import json
import os
from typing import List, Dict

DATA_DIR = os.getenv("RESOURCE_DATA_DIR", "data/resources")
INDEX_FILE = os.path.join(DATA_DIR, "index.json")
os.makedirs(DATA_DIR, exist_ok=True)


def load_index() -> List[Dict]:
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index: List[Dict]):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def export_index(path: str):
    index = load_index()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
    return path


def import_index(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError("Expected JSON array")
    index = load_index()
    index.extend(payload)
    save_index(index)
    return len(payload)
