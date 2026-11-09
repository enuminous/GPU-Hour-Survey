import json
import unittest
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "data/prices.json").read_text(encoding="utf-8"))
ROWS = DOC["quotes"]

class SurveyTests(unittest.TestCase):
    def test_schema_and_units(self):
        self.assertEqual(DOC["schema_version"], 1)
        self.assertEqual(DOC["currency"], "USD")
        self.assertEqual(DOC["quote_unit"], "USD per GPU-hour")
        self.assertTrue(DOC["not_live"])
        self.assertRegex(DOC["survey_date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_quotes_have_provenance_and_positive_numbers(self):
        for q in ROWS:
            with self.subTest(id=q["id"]):
                self.assertGreater(q["usd_per_gpu_hour"], 0)
                self.assertGreater(q["vram_gb"], 0)
                self.assertTrue(q["source_url"].startswith("https://"))
                self.assertRegex(q["checked_on"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertTrue(q["provider"] and q["model"] and q["variant"])
                self.assertIn(q["tier"], ("on-demand", "spot", "marketplace"))
                self.assertIn(q["price_kind"], ("posted", "from", "restricted", "market-median"))
                self.assertIn(q["minimum_gpus"], (None, *range(1, 129)))

    def test_unique_rows(self):
        self.assertEqual(len(ROWS), len({q["id"] for q in ROWS}))
        self.assertEqual(len(ROWS), len({(q["provider"], q["model"], q["tier"]) for q in ROWS}))

    def test_default_mean_has_only_fixed_ondemand(self):
        for q in ROWS:
            if q["in_default_average"]:
                self.assertEqual(q["tier"], "on-demand")
                self.assertEqual(q["price_kind"], "posted")

    def test_future_rates_not_silently_included(self):
        self.assertNotIn("Lambda", {q["provider"] for q in ROWS})

    def test_h100_baseline_replays(self):
        vals = [q["usd_per_gpu_hour"] for q in ROWS
                if q["model"] == "H100 80GB" and q["in_default_average"]]
        self.assertEqual(len(vals), 4)
        self.assertAlmostEqual(mean(vals), 4.025)
        self.assertAlmostEqual(median(vals), 4.20)

    def test_l40s_starting_rate_excluded(self):
        neb = [q for q in ROWS if q["provider"] == "Nebius"
               and q["model"] == "L40S 48GB" and q["tier"] == "on-demand"]
        self.assertEqual(len(neb), 1)
        self.assertFalse(neb[0]["in_default_average"])

    def test_h100_marketplace_separate(self):
        self.assertFalse(any(q["in_default_average"] for q in ROWS if q["tier"] != "on-demand"))

    def test_self_contained_build_in_sync(self):
        source = (ROOT / "template.html").read_text(encoding="utf-8")
        inline = (json.dumps(DOC, ensure_ascii=False, separators=(",", ":"))
                  .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))
        self.assertEqual((ROOT / "index.html").read_text(encoding="utf-8"),
                         source.replace("__SURVEY_DATA__", inline))

    def test_provider_diversity(self):
        self.assertGreaterEqual(len({q["provider"] for q in ROWS}), 5)
        self.assertGreaterEqual(len({q["model"] for q in ROWS}), 6)

if __name__ == "__main__":
    unittest.main()
