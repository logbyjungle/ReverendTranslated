from bot import translatewhole, startdriver
from flask import Flask, Response, redirect, render_template, stream_template, url_for
import subprocess
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument("--nodriver",action="store_true",help="disables webdriver")
parser.add_argument("--verbose",action="store_true",help="enables debug mode")
parser.add_argument("--nostore",action="store_true",help="disabled storing translated chapters")
parser.add_argument("--noread",action="store_true",help="disabled reading translated chapters")
parser.add_argument("--headful",action="store_true",help="disables headless mode")
args = parser.parse_args()

if not args.nodriver:
    startdriver(args.headful)

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
        for paragraph in translatewhole(chapter,lang,args):
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
