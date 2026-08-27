#!/bin/bash
cd /root/technocore-agent || exit 1
git checkout -q -- 'price-*.json' 2>/dev/null
git pull -q --rebase origin main || exit 1
LINE=$(python3 compute_price.py) || exit 1
DAY=$(date -u +%F)
git add "price-$DAY.json"
git diff --cached --quiet && { echo "$(date -u) $DAY no change"; exit 0; }
git commit -qm "compute-price $DAY"
git push -q origin main && echo "$(date -u) pushed: $LINE"
