"""Restore the *historical* starting dataset from the original standalone release.

This is NOT a price scraper and must not be used to refresh provider quotes.
It will overwrite data/prices.json; preserve newer revisions before running.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
match = re.search(r'<script type="application/json" id="survey-data">([\\s\\S]*?)</script>', html)
if not match:
    raise RuntimeError("Cannot find the historical embedded survey data")
data = json.loads(match.group(1))
if data.get("survey_date") != "2026-11-09" or len(data.get("quotes", [])) != 34:
    raise RuntimeError("Historical snapshot guard failed; not overwriting dataset")
(ROOT / "data/prices.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Restored", len(data["quotes"]), "historical quote records; NOT refreshed.")
