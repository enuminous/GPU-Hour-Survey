# Methodology and evidence limitations

**Survey date:** November 9, 2026 (UTC date).  
**Data:** [`data/prices.json`](data/prices.json).  
**Unit:** U.S. dollars per billed GPU-hour, using posted prices—not post-discount invoice costs.

## Headline statistic

For model family *g*, rental tier *t*, and provider *p*, select at most one eligible price `x[p,g,t]`, where eligibility is a fixed, publicly posted on-demand price not requiring an additional term, subscription, or reservation (as far as the pricing page discloses). Then:

```text
mean(g)   = sum(x[p,g,on-demand]) / number_of_distinct_providers
median(g) = middle of the sorted price sample
range(g)  = [min(price sample), max(price sample)]
```

The default uses `in_default_average=true` rows. Each provider is **equally weighted**, not weighted by offered inventory, transactions, bookings, uptime, GPU performance, or market share. For a GPU family with one qualifying provider, the site's “mean” is just the single source rate; it is **not a meaningful cross-provider market estimate**.

The “include indicative/restricted” toggle creates an **explicitly looser, non-comparable reference average** by including the extra rows in the selected rental tier. Never refer to this as a market-clearing price.

## Source records

| Provider | Original source | Handling |
|---|---|---|
| RunPod | https://www.runpod.io/pricing | Secure Cloud **Pods**, fixed per-GPU-hour quotes. Community Cloud or Serverless rates can differ. Pricing page reports an update of November 4, 2026. |
| Hyperstack | https://www.hyperstack.cloud/gpu-pricing | Published **On-Demand GPU Pricing** only; no reservation/spot mix. Specific variants noted. |
| DigitalOcean | https://docs.digitalocean.com/products/droplets/details/pricing/ | **On-Demand GPU Droplet Pricing**, not spot pricing or dedicated inference. |
| Nebius | https://nebius.com/prices | **On-demand GPU-hour effective October 1, 2026** (right-hand column) for HGX H100, H200, and B200. L40S “from” price is excluded from strict average. Separate preemptible “from” figures are spot-only. |
| Paperspace | https://docs.digitalocean.com/products/paperspace/pricing/ | H100 promotional **on-demand** price with 8-GPU SKU; other plans may require a subscription. These are flagged `restricted` and excluded by default. |
| Vast.ai | https://vast.ai/article/how-much-does-it-cost-to-rent-a-gpu-in-the-cloud-live-pricing-guide | **Marketplace offer medians**, not fixed on-demand quotes. The page showed a tape age around 392 hours when checked. Indicative only and explicitly separated from on-demand. |

**Excluded future schedule:** [Lambda pricing](https://lambda.com/pricing) displayed several prices labeled effective **November 16, 2026**. That effective date is in the future relative to this November 9 survey. We do not silently use future rates for the historical snapshot.

## Precision / comparability

- H100 80GB and A100 80GB *families* can contain different SXM, PCIe, HGX, and interconnect configurations. GPU performance, memory bandwidth, networking, CPU allocations, and billing units vary.
- Some published prices are GPU-hour *shares of mandatory multi-GPU servers*. They are not guaranteed single-GPU checkout rates. Minimum topology is unknown unless source documentation was explicit.
- The B200 examples mix some listed VRAM configurations; see quote-specific variant notes.
- Starting prices are lower bounds, not typical transaction prices.
- “Marketplace median” is a median of available offers reported by one provider, and **not** a provider's own fixed rental rate. It must not be aggregated with posted on-demand offers.
- USD rates may exclude taxes, included storage limits, egress, extra CPU/memory, commitments, subscription fees, and region-dependent availability. The dataset does not independently verify bookability.

## Independence and coverage

The dataset represents **selected advertised public prices**, not a random sample of every provider or an inventory-weighted census of all deployed GPUs. A cheaper provider may have no capacity, while a dearer price may include a service-level benefit. Not every family has two or more qualifying providers. Variation here is **not** a measure of statistically sampled national/global rental cost.

## Next steps toward a market index

1. Integrate authenticated / documented vendor pricing APIs where available, without violating scraping rules or terms.
2. Require a recent timestamp and explicit offer availability per quote.
3. Separate identical GPU variants, region, tenancy, preemptible availability, minimum GPU commitment, and network/storage bundles.
4. Calculate weighted indices only after independent inventory / executed transaction data are available.
5. Archive successive snapshots and compute directional changes with source-version pins.

**Status:** A reproducible surveyed-price dashboard. **Not:** a live price aggregator, a guaranteed purchasable quote, or a representative transaction-level market index.