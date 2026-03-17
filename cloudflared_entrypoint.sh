#!/bin/sh

REPO_URL=$(grep 'url =' /tmp/gitconfig | head -n1 | awk '{print $3}')
git clone "${REPO_URL}" /repo
cd /repo
git checkout tunnel

touch /tmp/tunnel.log
cloudflared tunnel --url http://nginx:80 2>&1 | tee /tmp/tunnel.log &
CF_PID=$!

while true; do
    URL=$(grep -o 'https://[-a-z0-9]*\.trycloudflare\.com' /tmp/tunnel.log | head -n1)
    if [ ! -z "$URL" ]; then
        break
    fi
    sleep 1
done

git config --global user.name "${USERNAME}"
git config --global user.email "${USEREMAIL}"
git remote set-url origin "https://${GITTOKEN}@github.com/${USERNAME}/ReverendTranslated.git"

echo "$URL" > address.txt
git add address.txt

LASTMSG=$(git log -1 --pretty=%s)
if [ "$LASTMSG" = "update tunnel address" ]; then
    git commit --amend --no-edit
else
    git commit -m "update tunnel address"
fi

git push --force-with-lease

wait $CF_PID
