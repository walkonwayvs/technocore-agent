#!/bin/bash
cd /root/technocore-agent || exit 1
git checkout -q -- 'data/price-*.json' 2>/dev/null
git pull -q --rebase origin main || exit 1
LINE=$(python3 compute_price.py) || exit 1
DAY=$(date -u +%F)

python3 agent.py say builders "$LINE" >/dev/null 2>&1
python3 agent.py say d-walkonwayvs "$LINE" >/dev/null 2>&1

# commit every 4th day only
if [ $(( $(date -u +%s) / 86400 % 4 )) -ne 0 ]; then
  echo "$(date -u) posted, holding commit: $LINE"
  exit 0
fi

git add data/
git diff --cached --quiet && { echo "$(date -u) no change"; exit 0; }
COUNT=$(git diff --cached --name-only | wc -l)
git commit -qm "compute-price: $COUNT days through $DAY"
git push -q origin main && echo "$(date -u) pushed $COUNT days + posted: $LINE"
