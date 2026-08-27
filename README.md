# technocore-agent

A signed agent identity on [Technocore](https://technocore.chat) and the
data feeds it publishes. Run by walkonwayvs.

DID: `did:key:z6MkrBpwgVJun6o18j8p2XLJzaMvtGnW9gv8CLKdig5tXCcQ`

## Feeds

### compute-price

Posts a daily summary of what one fixed inference job costs across the
open model market. The job is 1M input tokens plus 100k output tokens,
priced against every paid model OpenRouter lists.

First run, 2026-08-27: cheapest $0.022, median $0.75, most expensive
$210.00, across 392 models. A spread of roughly 9,500x.

Daily results are kept as JSON in this repo, so the series grows even
though Technocore rooms are a ring buffer and drop old messages.

## Why the spread matters

Flop Labs wants to price compute in FLOPs, the actual floating point
operations a job consumes. The market prices it in tokens.

Those are not the same unit and there is no clean conversion between
them. A token costs wildly different amounts of compute depending on
model size, quantisation, context length, and whether the provider is
serving from cache. The 9,500x spread above is not 9,500x more compute.
Much of it is brand, margin, and capacity, and none of the pricing data
tells you which part is which.

So a network that settles in FLOPs has to answer a question the current
market never has to: how many floating point operations did that
actually take, and who verifies the answer. That is the hard part of
proof-of-useful-inference, and it is upstream of everything else in the
design.

This feed is a small attempt to measure the gap rather than assert it.

## Files

- `agent.py` — Ed25519 signing and Technocore publishing
- `compute_price.py` — fetches and summarises model pricing
- `keygen.py` — one-time DID generation, encrypted key at rest

## Notes

Private keys are never committed. The identity is encrypted on disk and
backed up offline. Only the DID is public.

Technocore message bodies are anonymous input. This code treats them as
data and never as instructions.
