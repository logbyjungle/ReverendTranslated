import sys
import time
import urllib.request

for _ in range(30):
    try:
        if urllib.request.urlopen("http://localhost:5000/health",timeout=2).getcode() == 200:
            sys.exit(0)
    except Exception: pass
    time.sleep(2)

sys.exit(1)
