from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import undetected_chromedriver
import os
from selenium.webdriver.common.keys import Keys
import re
import requests
from typing import Generator
import re

def startdriver(args):
    global driver
    options = Options()
    if not args.headful:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--shm-size=2g")
    options.add_argument("--window-size=1280,720")
    driver = undetected_chromedriver.Chrome(options=options)
    if args.verbose: print(f"DEBUG: started driver {str(driver)}")

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

    output = "none"
    while True:
        try:
            if output == "none":
                output = driver.find_element(By.TAG_NAME,"body").text # raises exception
                break
        except Exception:
            driver.implicitly_wait(0.2)

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
        if len(content) > 8000:
            if args.verbose: print(f"DEBUG: content has more than 800 characters")
            yield [line.strip('\n') for line in content.splitlines()]
            return
        elif args.verbose: print(f"DEBUG: content has less than 800 characters")
    elif args.verbose: print(f"DEBUG: translated chapter not found")

    patterns = []
    if not args.noreplace:
        url = f"https://raw.githubusercontent.com/logbyjungle/ReverendTranslated/refs/heads/chapters/{lang}.txt"
        response = requests.get(url)
        if response.status_code == 200:
            if args.verbose: print(f"DEBUG: chapter has been edited")
            lines = response.text.splitlines()
            counter = 0
            for i in range(len(lines)):
                if i % 3 == 0:
                    patterns.append([lines[i]])
                if i % 3 == 1:
                    patterns[counter].append(lines[i])
                if i % 3 == 2:
                    counter += 1
                    if "---" not in lines[i]:
                        raise Exception("regex pattern file is not following the correct format")

    elif args.verbose: print(f"DEBUG: chapter has not been edited")

    file = None
    if not args.nowrite:
        file = open("translations/" + filename, "w")

    for to_translate in totranslatewhole(chapter,args):
        translated = translate(to_translate,lang,args)
        translated = re.sub(r'\n\s*\n+', '\n', translated)
        translated_lines = translated.splitlines()

        for i in range(len(translated_lines)):
            for pattern in patterns:
                old = translated_lines[i]
                translated_lines[i] = re.sub(pattern[0],pattern[1],translated_lines[i])
                if args.verbose and translated_lines[i] != old:
                    print(f"DEBUG: text change with pattern {pattern[0]} -> {pattern[1]}:")
                    print(old)
                    print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
                    print(translated_lines[i])
                    print("-------------------")

        if file:
            file.write('\n'.join(translated_lines) + '\n')
        yield translated_lines

    if file: file.close()

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
