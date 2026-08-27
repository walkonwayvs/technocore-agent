import re, sys
from datetime import datetime, timezone

LOG = "/home/lapper/sail-agent-03/.sail/agent.log"
rates = decision = None
errors = []

for line in open(LOG, errors="replace"):
    line = line.strip()
    if line.startswith("[agent] rates:"):
        rates = line.split("rates:", 1)[1].strip()
        decision = None
    elif "fetchRates:" in line:
        m = re.search(r"fetchRates: (\w+) error", line)
        if m:
            if rates is not None and decision is not None:
                errors = []
            errors.append(m.group(1))
    elif line.startswith(("[agent] cooldown:", "[agent] no rotate:", "[agent] rotat", "[agent] current venue")):
        decision = line.split("] ", 1)[1]

if not rates:
    sys.exit("no rates line found")

verdict = "held" if decision and "skipping" in decision else "rotated"
why = decision.split("—")[0].strip() if decision else "unknown"
why = re.sub(r"\s+", " ", why)
day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
err = f" | unreadable: {','.join(errors)}" if errors else ""

print(f"sail-yield {day} | usdc supply rates on base: {rates}{err} "
      f"| {verdict} — {why} | 0.5pp threshold, 24h cadence")
