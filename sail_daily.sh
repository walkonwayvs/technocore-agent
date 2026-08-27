#!/bin/bash
cd /home/lapper/flop-agent || exit 1
DAY=$(date -u +%F)
[ -f ".posted-$DAY" ] && exit 0
LINE=$(python3 sail_feed.py) || exit 1
python3 agent.py say builders "$LINE" >/dev/null 2>&1
touch ".posted-$DAY"
act_notify=0
case "$LINE" in *"| held"*) ;; *) act_notify=1 ;; esac
case "$LINE" in *unreadable*) act_notify=1 ;; esac
MSG=$(python3 -c "
import re,sys
l=sys.argv[1]
rates=re.findall(r'(\w+)=([\d.]+)%', l)
best=re.search(r'best (\w+) ([\d.]+)%', l)
act='held' if '| held' in l else 'ROTATED'
bad=re.search(r'unreadable: ([\w,]+)', l)
out=f\"**[technocore] sail-yield feed** — {act}\"
if best: out += f\" in {best.group(1)} at {best.group(2)}%\"
out += '\\n' + '  '.join(f'{v} {r}%' for v,r in rates)
if bad: out += f'\\n_no rate from {bad.group(1)}_'
print(out)
" "$LINE")
if [ "$act_notify" = "1" ]; then
curl -s -X POST "https://discord.com/api/webhooks/1496397378767294605/Mm65RSVFeSBpdn_ZNHptmYif4IlsBKAs-dpy8NJjuJyjUsILTV7HB_4xrdT5Yyxm2ZDC" \
  -H "Content-Type: application/json" \
  --data "$(python3 -c "import json,sys; print(json.dumps({'content': sys.argv[1]}))" "$MSG")" >/dev/null
fi
echo "$(date -u) posted: $LINE"
