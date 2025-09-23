from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
import urllib.parse
import undetected_chromedriver
import os
from bs4 import BeautifulSoup

options = Options()
driver = undetected_chromedriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options, version_main=139
    )

def translate(text,lang,quit = 1):

    driver.get(f"https://translate.google.com/?sl=en&tl={lang}&text={text}&op=translate")

    try:
        accept_all = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept all')]"))
        ) # raises an exception btw

        accept_all.click()
    except Exception:
        pass
    driver.implicitly_wait(1)

    copy_elem = WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Copy translation"]'))
    )
    driver.implicitly_wait(1)
    copy_elem.click()
    time.sleep(1)
    # print(pyperclip.paste())

    # driver.implicitly_wait(1)

    if quit:
        driver.quit()

    return pyperclip.paste()


def translatewhole(text,lang,quit=1):
    translation = ""
    splits = text.split("\n\n\n") 
    splits_encoded = [urllib.parse.quote(split) for split in splits]

    divisor = urllib.parse.quote("\n\n\n")

    start = 0
    chars = 0
    for i in range(len(splits)):
        if chars + len(splits_encoded[i]) > 4500:
            to_translate = ""
            for j in range(start,i):
                to_translate += splits_encoded[j]
                to_translate += divisor
            translation += translate(to_translate,lang,0)
            start = i
            chars = 0
        elif i == len(splits)-1:
            to_translate = ""
            for j in range(start,i):
                to_translate += splits_encoded[j]
                to_translate += divisor
            translation += translate(to_translate,lang,0)
        else:
            chars += len(splits_encoded[i])
    if quit:
        driver.quit()
    return translation
    

def scrape_chapter(chapter,quit=1):

    os.makedirs("sources",exist_ok=True)
    filename = "sources/" + str(chapter) + ".html"
    if not os.path.isfile(filename):
        driver.get(f"https://mananovel.com/novel/reverend-insanity-11/chapter/{chapter}")

        with open(filename, "w") as file:
            file.write(driver.page_source)

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        all_text = [p.text for p in paragraphs]

        if quit:
            driver.quit()

        return "\n\n\n".join(all_text)
    else:
        with open(filename) as file:
            html = file.read()
            soup = BeautifulSoup(html, "html.parser")
            paragraphs = [p.get_text() for p in soup.find_all("p")]

        if quit:
            driver.quit()

        return "\n\n\n".join(paragraphs)

def translate_and_store(chapter,lang):
    os.makedirs("translations",exist_ok=True)
    filename = lang + "-" + str(chapter) + ".txt"
    if not os.path.isfile("translations/" + filename):
        with open("translations/" + filename, "w") as file:
            file.write(translatewhole(scrape_chapter(chapter,0),lang))

translate_and_store(1,"it")
