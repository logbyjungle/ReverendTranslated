import sys
import time
import urllib.request

for _ in range(30):
    try:
        code = urllib.request.urlopen(
            "http://localhost:5000/health", timeout=2
        ).getcode()
        if code == 200:
            sys.exit(0)
        else:
            print(f"GOT STATUS CODE {code}")
    except Exception as e:
        print(e)
    time.sleep(2)

sys.exit(1)
