from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import undetected_chromedriver
import os
from pathlib import Path
from selenium.webdriver.common.keys import Keys
import re
import subprocess
import requests
from typing import Generator

def in_docker() -> bool:
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())

if in_docker():
    os.environ["DISPLAY"] = ":99"

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

def startdriver(head):
    global driver
    options = Options()
    if not head:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--shm-size=2g")
    options.add_argument("--window-size=1280,720")
    driver = undetected_chromedriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options , version_main=get_chrome_version()
    )

def translate(text,lang,args) -> str:

    driver.get(f"https://translate.google.com/?sl=en&tl={lang}&text={text}&op=translate")

    try:
        try:
            accept_all = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
            ) # raises exception

            if args.verbose: print(f"DEBUG: accept_all found")
            accept_all.click()
        except Exception:
            pass
        _ = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Copy translation"]'))
        ) # raises exception
        if args.verbose: print(f"DEBUG: copy translation found")
    except Exception:
        try:
            accept_all = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
            ) # raises exception
            if args.verbose: print(f"DEBUG: accept_all found")

            accept_all.click()
        except Exception:
            pass

        elem = driver.find_element(By.TAG_NAME, "html")
        elem.send_keys(Keys.END)
        if args.verbose: print(f"DEBUG: scrolling to the bottom of the page")
        _ = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Copy translation"]'))
        ) # raises exception
        if args.verbose: print(f"DEBUG: copy translation found")

    output = driver.find_element("tag name","body").text
    outputs = []
    start = False
    lines = output.splitlines()
    for line in lines:
        if line == "Translation result": 
            start = True
        elif start:
            if line == "Send feedback":
                break
            elif line and line[0] == ' ':
                outputs[len(outputs)-1] += line
            else:
                outputs.append(line)

    return "\n".join(outputs)

def scrape_chapter(chapter,args) -> str:
    url = f"https://raw.githubusercontent.com/logbyjungle/ReverendTranslated/refs/heads/chapters/chapters/{chapter}.txt"
    response = requests.get(url)
    if args.verbose: print(f"DEBUG: request executed to chapter stored on github with status code {response.status_code}")
    return response.text

def translatewhole(chapter,lang,args) -> Generator[list[str]]:
    os.makedirs("translations",exist_ok=True)
    filename = lang + "-" + str(chapter) + ".txt"
    if args.verbose: print(f"DEBUG: using filename {filename}")

    if os.path.isfile("translations/" + filename) and not args.noread:
        if args.verbose: print(f"DEBUG: translated chapter found")
        with open("translations/" + filename, 'r') as file:
            content = file.read()
        if len(content) > 500:
            if args.verbose: print(f"DEBUG: content has more than 500 characters")
            yield [line.strip('\n') for line in content.splitlines()]
            return
        elif args.verbose: print(f"DEBUG: content has less than 500 characters")
    elif args.verbose: print(f"DEBUG: translated chapter not found")

    url = f"https://raw.githubusercontent.com/logbyjungle/ReverendTranslated/refs/heads/chapters/{lang}-{chapter}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        if args.verbose: print(f"DEBUG: chapter has been edited")
        yield response.text.splitlines()
        return
    elif args.verbose: print(f"DEBUG: chapter has not been edited")
    with open("translations/" + filename, "w") as file:
        for to_translate in totranslatewhole(chapter,args):
            translated = translate(to_translate,lang,args)
            translated = re.sub(r'\n\s*\n+', '\n', translated)
            translated_lines = translated.splitlines()
            if not args.nostore:
                file.write('\n'.join(translated_lines) + '\n')
            yield translated_lines

def totranslatewhole(chapter,args) -> list[str]:
    text = scrape_chapter(chapter,args)

    splits = text.split("\n\n\n") 
    splits_encoded = [urllib.parse.quote(split) for split in splits]

    divisor = urllib.parse.quote("\n\n\n")

    start = 0
    chars = 0
    to_translate_whole = []
    for i in range(len(splits)):
        if chars + len(splits_encoded[i]) > 4500:
            to_translate = ""
            for j in range(start,i):
                to_translate += splits_encoded[j]
                to_translate += divisor
            to_translate_whole.append(to_translate)
            start = i
            chars = 0
        elif i == len(splits)-1:
            to_translate = ""
            for j in range(start,i+1):
                to_translate += splits_encoded[j]
                to_translate += divisor
            to_translate_whole.append(to_translate)
        else:
            chars += len(splits_encoded[i])
    return to_translate_whole
