#!/bin/bash
URL="https://technocore.chat/kv/did-e4/06ba93b27bcb08/set/did%3Akey%3Az6MkrBpwgVJun6o18j8p2XLJzaMvtGnW9gv8CLKdig5tXCcQ%20%7C%20walkonwayvs%20%7C%20validator%20operator%2C%20base%20agents"
HOOK="${DISCORD_WEBHOOK}"
R=$(curl -s --max-time 30 "$URL")
echo "$(date -u) :: $R" >> /root/flop-refresh.log

case "$R" in
  ok\ did-e4/*) exit 0 ;;
esac

# only reached if the write did not return ok
curl -s -X POST "$HOOK" -H "Content-Type: application/json" \
  --data "$(python3 -c "import json,sys;print(json.dumps({'content':'**[technocore] DID note refresh FAILED**\n'+sys.argv[1][:300]+'\nThe note expires 7 days after the last successful write.'}))" "$R")" >/dev/null
