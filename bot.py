from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import urllib.parse
import undetected_chromedriver
import os
from pathlib import Path
from selenium.webdriver.common.keys import Keys
import re
import subprocess
import time
import requests

def in_docker():
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())

if in_docker():
    os.environ["DISPLAY"] = ":99"

running = 0

def get_chrome_version():
    try:
        # Works for both google-chrome-stable and chromium
        output = subprocess.check_output(["google-chrome-stable", "--version"]).decode()
    except FileNotFoundError:
        output = subprocess.check_output(["chromium", "--version"]).decode()
    match = re.search(r"(\d+)\.", output)
    if match:
        version = match.group(1)
    else:
        raise Exception("chrome driver version not found")
    print("using chrome driver version " + version)
    return int(version)

def startdriver():
    global running
    global driver
    if not running:
        options = Options()
        # using headless mode breaks everything
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--shm-size=2g")
        options.add_argument("--window-size=1280,720")
        driver = undetected_chromedriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options , version_main=get_chrome_version()#, version_main=139
        )
        running = 1

def translate(text,lang):

    startdriver()

    driver.get(f"https://translate.google.com/?sl=en&tl={lang}&text={text}&op=translate")

    try:
        try:
            accept_all = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
            ) # raises an exception btw

            accept_all.click()
        except Exception:
            pass
        copy_elem = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Copy translation"]'))
        )
    except Exception:
        try:
            accept_all = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
            ) # raises an exception btw

            accept_all.click()
        except Exception:
            pass
        # goes to bottom of the page
        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        copy_elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Copy translation"]'))
        ) # raises exception

    copy_elem.click()
    if not pyperclip.paste():
        time.sleep(1)
        if not pyperclip.paste():
            raise Exception("Failed to copy translation")

    return pyperclip.paste()

def scrape_chapter(chapter):
    url = f"https://raw.githubusercontent.com/logbyjungle/ReverendTranslated/refs/heads/chapters/chapters/{chapter}.txt"
    response = requests.get(url)
    return response.text

def translatewhole(chapter,lang):
    text = scrape_chapter(chapter)
    os.makedirs("translations",exist_ok=True)
    filename = lang + "-" + str(chapter) + ".txt"

    if os.path.isfile("translations/" + filename):
        with open("translations/" + filename, 'r') as file:
            content = file.read()
        if len(content) > 500:
            yield [line.strip('\n') for line in content.splitlines()]
            return

    url = f"https://raw.githubusercontent.com/logbyjungle/ReverendTranslated/refs/heads/chapters/{lang}-{chapter}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        yield response.text
        return

    startdriver()

    splits = text.split("\n\n\n") 
    splits_encoded = [urllib.parse.quote(split) for split in splits]

    divisor = urllib.parse.quote("\n\n\n")

    start = 0
    chars = 0
    with open("translations/" + filename, "w") as file:
        for i in range(len(splits)):
            if chars + len(splits_encoded[i]) > 4500:
                to_translate = ""
                for j in range(start,i):
                    to_translate += splits_encoded[j]
                    to_translate += divisor
                line_s = translate(to_translate,lang)
                line_s = re.sub(r'\n\s*\n+', '\n', line_s)
                lines = line_s.splitlines()
                file.write('\n'.join(lines) + '\n')
                yield lines
                start = i
                chars = 0
            elif i == len(splits)-1:
                to_translate = ""
                for j in range(start,i+1):
                    to_translate += splits_encoded[j]
                    to_translate += divisor
                lines = translate(to_translate,lang)
                lines = re.sub(r'\n\s*\n','\n',lines)
                lines = lines.splitlines()
                file.write('\n'.join(lines) + '\n')
                yield lines
            else:
                chars += len(splits_encoded[i])
