from bot import translate_and_store
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/<lang>/<chapter>")
def page(lang, chapter):
    translate_and_store(chapter,lang)

    with open("translations/" + lang + "-" + chapter + ".txt", "r") as file:
        content = file.read()

    return render_template("index.html",chapter=chapter,content=content)

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
