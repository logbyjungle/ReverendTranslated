#!/bin/sh
set -e

cloudflared tunnel --url http://nginx:80 2>&1 | tee /tmp/tunnel.log &
CF_PID=$!

while true; do
    URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare\.com' /tmp/tunnel.log | head -n1)
    if [ ! -z "$URL" ]; then
        break
    fi
    sleep 1
done

echo "$URL" > address.txt

git config --global user.name "${USERNAME}"
git config --global user.email "${USEREMAIL}"
git remote set-url origin "https://${GITTOKEN}@github.com/${USERNAME}/ReverendTranslated.git"

LASTMSG=$(git log -1 --pretty=%s)
if [ "$LASTMSG" = "update tunnel address" ]; then
    git reset --soft HEAD~1
fi

git add address.txt
git commit -m "update tunnel address"
git push

wait $CF_PID
