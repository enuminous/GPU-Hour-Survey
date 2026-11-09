"""Build standalone offline index.html from canonical auditable price records."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
payload = json.loads((ROOT / "data/prices.json").read_text(encoding="utf-8"))
source = (ROOT / "template.html").read_text(encoding="utf-8")
assert source.count("__SURVEY_DATA__") == 1
inline = (json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
          .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))
(ROOT / "index.html").write_text(source.replace("__SURVEY_DATA__", inline), encoding="utf-8")
print("Built index.html with", len(payload["quotes"]), "quote records")
