from bot import translate_and_store, startdriver
from flask import Flask, render_template

app = Flask(__name__)

with open("languages.txt","r") as file:
    langs = eval(file.read())

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
    startdriver()
    app.run(debug=True,use_reloader=False,host="0.0.0.0")
