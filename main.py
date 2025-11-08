from bot import translatewhole, startdriver
from flask import Flask, Response, redirect, render_template, stream_template, url_for
import subprocess
import sys

app = Flask(__name__)

with open("languages.txt","r") as file:
    langs = eval(file.read())

def get_version():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "Unknown commit"

if len(sys.argv) < 2: # adding anything after "python main.py" causes the program to not start selenium
    startdriver()

@app.route("/",methods=["GET"])
def home():
    return render_template("main.html", mapping=langs, version=get_version())

@app.route("/api/<lang>/<chapter>",methods=["GET"])
def call(lang,chapter):
    if chapter not in [str(i) for i in range (1,2335)]:
        return redirect(url_for("home"))

    if lang not in langs.values():
        return redirect(url_for("home"))

    def generate():
        for paragraph in translatewhole(chapter,lang):
            yield ('\n'.join(paragraph) + '\n').encode('UTF-8')
    return Response(generate(),mimetype='text/plain',direct_passthrough=True)

@app.route("/<lang>/<chapter>",methods=["GET"])
def page(lang, chapter):
    if chapter not in [str(i) for i in range (1,2335)]:
        return redirect(url_for("home"))

    if lang not in langs.values():
        return redirect(url_for("home"))

    return stream_template("chapter.html",chapter=chapter)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False,host="0.0.0.0")
