#!/bin/bash
cd /root/technocore-agent || exit 1
git checkout -q -- 'data/price-*.json' 2>/dev/null
git pull -q --rebase origin main || exit 1
LINE=$(python3 compute_price.py) || exit 1
DAY=$(date -u +%F)
git add "data/price-$DAY.json"
git diff --cached --quiet && { echo "$(date -u) $DAY no change"; exit 0; }
git commit -qm "compute-price $DAY"
python3 agent.py say builders "$LINE" >/dev/null 2>&1
python3 agent.py say d-walkonwayvs "$LINE" >/dev/null 2>&1
git push -q origin main && echo "$(date -u) pushed + posted: $LINE"
