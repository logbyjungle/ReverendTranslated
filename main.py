from bot import translatewhole, startdriver
from flask import Flask, Response, redirect, render_template, stream_template, url_for
import subprocess
import argparse
from functools import wraps

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
parser.add_argument("--nowrite",action="store_true",help="disabled storing translated chapters")
parser.add_argument("--noread",action="store_true",help="disabled reading translated chapters")
parser.add_argument("--headful",action="store_true",help="disables headless mode")
parser.add_argument("--noreplace",action="store_true",help="disables replacing text using translation regex")
args,_ = parser.parse_known_args()

if not args.nodriver:
    while True:
        try:
            startdriver(args)
            break
        except Exception as e:
            print("failed to start driver due to error " + str(e))

def validity_check(func):
    @wraps(func)
    def wrapper(lang,chapter):
        if chapter not in [str(i) for i in range (1,2335)]:
            if args.verbose: print(f"DEBUG: selected chapter not in range 1-2334")
            return redirect(url_for("home"))
        elif lang not in langs.values():
            if args.verbose: print(f"DEBUG: selected language not in languages list")
            return redirect(url_for("home"))
        return func(lang,chapter)
    return wrapper

@app.route("/",methods=["GET"])
def home():
    return render_template("main.html", mapping=langs, version=get_version())

@app.route("/api/<lang>/<chapter>",methods=["GET"])
@validity_check
def call(lang,chapter):
    if not args.nodriver:
        def generate():
            for paragraph in translatewhole(chapter,lang,args):
                yield ('\n'.join(paragraph) + '\n').encode('UTF-8')
        return Response(generate(),mimetype='text/plain',direct_passthrough=True)
    else:
        return "driver disabled with --nodriver"

@app.route("/<lang>/<chapter>",methods=["GET"])
@validity_check
def page(lang, chapter):
    _ = lang # suppresses unused lang warning
    return stream_template("chapter.html",chapter=chapter)

@app.route("/health",methods=["GET"])
def health():
    return "OK",200

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False,host="0.0.0.0")
