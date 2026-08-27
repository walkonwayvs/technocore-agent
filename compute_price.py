import json, statistics, sys, urllib.request
from datetime import datetime, timezone

IN, OUT = 1_000_000, 100_000

def fetch():
    r = urllib.request.Request("https://openrouter.ai/api/v1/models",
                               headers={"User-Agent": "curl/8.0"})
    return json.load(urllib.request.urlopen(r, timeout=30))["data"]

rows = []
for m in fetch():
    try:
        p, c = float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])
    except (KeyError, TypeError, ValueError):
        continue
    cost = p * IN + c * OUT
    if cost > 0:
        rows.append((cost, m["id"]))

rows.sort()
lo, hi = rows[0], rows[-1]
med = statistics.median(c for c, _ in rows)
day = datetime.now(timezone.utc).strftime("%Y-%m-%d")

line = (f"compute-price {day} | job: 1M in + 100k out | "
        f"min ${lo[0]:.4f} ({lo[1]}) | median ${med:.4f} | "
        f"max ${hi[0]:.2f} ({hi[1]}) | spread {hi[0]/lo[0]:.0f}x | "
        f"{len(rows)} paid models | source openrouter | "
        f"priced per token, not per FLOP")
print(line)
json.dump({"date": day, "job": {"input": IN, "output": OUT},
           "min": lo[0], "min_model": lo[1], "median": med,
           "max": hi[0], "max_model": hi[1], "n": len(rows)},
          open(f"data/price-{day}.json", "w"), indent=2)
