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
from bs4 import BeautifulSoup
from pathlib import Path
from selenium.webdriver.common.keys import Keys
import re

def in_docker():
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or (cgroup.is_file() and 'docker' in cgroup.read_text())

if in_docker():
    os.environ["DISPLAY"] = ":99"

running = 0

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
            service=Service(ChromeDriverManager().install()), options=options, version_main=139
        )
        running = 1

def stopdriver():
    global running
    global driver
    if running:
        driver.quit()
        running = 0

def translate(text,lang,quit = 1):

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
        raise Exception("Failed to copy translation")

    if quit:
        stopdriver()

    return pyperclip.paste()

def scrape_chapter(chapter,quit=1):
    os.makedirs("sources",exist_ok=True)
    filename = "sources/" + str(chapter) + ".html"
    if not os.path.isfile(filename):
        startdriver()
        driver.get(f"https://fantasylibrary.ink/novel/reverend-insanity-11/chapter/{chapter}")

        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        with open(filename, "w") as file:
            file.write(driver.page_source)

    with open(filename) as file:
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        if soup.title is not None and soup.title.string is not None:
            paragraphs.insert(0,soup.title.string[20:-18])

    if quit:
        stopdriver()

    return "\n\n\n".join(paragraphs)

def translatewhole(chapter,lang,quit=1):
    text = scrape_chapter(chapter,0)
    os.makedirs("translations",exist_ok=True)
    filename = lang + "-" + str(chapter) + ".txt"

    if os.path.isfile("translations/" + filename):
        with open("translations/" + filename, 'r') as file:
            return file.readlines()

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
                line_s = translate(to_translate,lang,0)
                line_s = re.sub(r'\n\s*\n+', '\n', line_s)
                lines = line_s.splitlines()
                lines = [line for line in lines if "fantasylibrary" not in line and "🎉" not in line and "Reverend Insanity" not in line]
                file.writelines(lines)
                yield lines
                start = i
                chars = 0
            elif i == len(splits)-1:
                to_translate = ""
                for j in range(start,i+1):
                    to_translate += splits_encoded[j]
                    to_translate += divisor
                lines = translate(to_translate,lang,0).splitlines()
                lines = [line for line in lines if "fantasylibrary" not in line and "🎉" not in line and "Reverend Insanity" not in line]
                file.writelines(lines)
                yield lines
            else:
                chars += len(splits_encoded[i])
    if quit:
        stopdriver()
