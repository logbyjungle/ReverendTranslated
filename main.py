from bot import translate_and_store, stopdriver, startdriver
from flask import Flask, render_template
import threading
import time

app = Flask(__name__)
last_request_time = time.time()

with open("languages.txt","r") as file:
    langs = eval(file.read())

def monitor_inactivity():
    global last_request_time
    while True:
        time.sleep(10)
        if time.time() - last_request_time > 600:
            print("stopped driver after 10m")
            stopdriver()
            last_request_time = time.time()

@app.before_request
def driverstart():
    global last_request_time
    last_request_time = time.time()
    print("starting driver due to page loading")
    startdriver()

@app.route("/")
def home():
    return render_template("main.html", mapping=langs)

@app.route("/<lang>/<chapter>")
def page(lang, chapter):
    if chapter not in [str(i) for i in range (1,2335)]:
        return "What chapter is " + str(chapter) + " exactly?"

    if lang not in langs.values():
        return "What language is " + lang + " exactly?"

    translate_and_store(chapter,lang,0)

    with open("translations/" + lang + "-" + chapter + ".txt", "r") as file:
        content = file.read()

    return render_template("chapter.html",chapter=chapter,content=content)

if __name__ == '__main__':
    threading.Thread(target=monitor_inactivity, daemon=True).start()
    app.run(debug=True,use_reloader=False,host="0.0.0.0")
