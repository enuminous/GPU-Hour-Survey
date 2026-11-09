# GPU Hour Survey

**A simple, reproducible, source-linked survey of published hourly GPU rental rates.**

This rebuilt ZIP includes a fully self-contained `index.html` that can be opened offline. All 34 historical quotes are embedded; no network requests are made by the dashboard. External source links will need internet.

Open [`index.html`](index.html) locally, or publish this folder to GitHub Pages. No build tool, hosting service, JavaScript dependency, API key, or analytics are required to view the survey.

**Initial snapshot:** November 9, 2026. **34 quotes**, **6 providers**, **8 GPU families**, across on-demand, marketplace, and spot categories. These are *advertised* rates, not live inventory confirmations.

## What it does

- Compares prices on a common **USD / GPU-hour** basis.
- Lets readers choose GPU family and rental market (on-demand, marketplace medians, spot).
- Calculates the **equal-provider sample arithmetic mean**, sample median, minimum, maximum, and provider count.
- Shows source URLs, model variants, quote types, the review date, and non-comparable offers.
- Projects GPU-hours × GPU count × survey mean, and exports CSV/JSON.
- Shows a model-by-model summary. All app code and dataset are inspectable.

## Data policy

Default mean: one **fixed, publicly posted, on-demand** price per provider for the selected GPU family. Excluded by default: spot/preemptible prices, marketplace offer medians, "from" rates, subscription/contract-restricted rates and quote-only pricing. The toggle can include indicative offers, but the result is explicitly not like-for-like.

A *GPU family* is not an exact SKU: H100 SXM, PCIe, and HGX installations may differ substantially in throughput, GPU count, and networking. The comparison is a rough advertised-price indicator, **not a transaction-volume-weighted industry average**.

Because quotes age, the website intentionally labels itself a **static price snapshot** rather than claiming to fetch live real-time rates. Some provider pages may display a new price before the snapshot is revised. See [METHODOLOGY.md](METHODOLOGY.md).

## Update the survey

1. Open the source URL of each affected row in [`data/prices.json`](data/prices.json).
2. Inspect current published price and terms, including effective date, region, multi-GPU minimum, and interruptibility.
3. Edit `usd_per_gpu_hour`, `checked_on`, `quote_observed_on`, `note`, `price_kind`, and `in_default_average` as justified. Never update a check date for a page you have not actually inspected.
4. Update the top-level `survey_date` to the last full review date (or retain the older survey date until reviewed).
5. Run:

```sh
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
```

6. Review the changed files and source links before publishing.

The seed script is the historical November 9 dataset, **not an updater**. Do not rerun `scripts/seed_data.py` after making new editorial revisions, because it resets the dataset to its initial snapshot.

## GitHub Pages

Create a public repository and upload the **contents** of this project to the repo root. Then open **Settings → Pages → Deploy from a branch → main / (root)**. `index.html` is a complete self-contained single-file site. The repository also contains the editable source template and machine-readable data.

## Reproducibility

- Python standard library; no dependencies.
- CI rebuilds `index.html` and checks whether the committed generated file matches the dataset.
- Tests assert price units, uniqueness of provider/model/tier/quote-kind, source provenance, inclusion rules, and stable statistical calculations.
- All source URLs point to the original providers' pages.

## Sources

RunPod, Hyperstack, DigitalOcean, Nebius, Paperspace, and Vast.ai. See [METHODOLOGY.md](METHODOLOGY.md) and `data/prices.json` for the direct links and qualifications. **Lambda is intentionally excluded:** the pricing card inspected November 9 advertised a schedule effective November 16, 2026, so it cannot safely be treated as the current November 9 quote.

## License

MIT for the code and survey presentation. Individual provider names and published prices belong to their respective sources. Please independently verify all prices before purchase.