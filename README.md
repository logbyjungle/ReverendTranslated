# ReverendTranslated

<p align="center">
    <img src="static/icon.png" alt="Perseverance" width="200">
</p>
<p align="center">
    <i>The translation is not perfect of course, but it is for sure better than those MTL sites</i><br>
    <i>The version of RI that is translated is in english, instead of the original chinese version, this might cause a further loss in meaning</i><br>
    <i>Thats why i'll be trying to add an option to choose which version to choose</i><br>
</p>

---

In order to be run locally you just have to:
```sh
git clone https://github.com/logbyjungle/ReverendTranslated.git
cd ReverendTranslated
pip install -m requirements.txt # use a venv if you want to
python main.py
```
and then enter the site at `localhost:5000`
**OR you can just use a docker container with port 5000 open 🐋**

This is a site hosted utilizing flask, it takes pages of RI's chapters from other sites and translate them by using google translate via selenium

The objective to be reached is spreading *Gu Zhen Ren*'s work across the globe by making sure everyone can read it

As of now the project is still not really made to be used:
1. the site lacks a good UI
2. the requests arent handled in parallel due to selenium's limitations, this means that the entire way the project work will have to be revolutionized
3. there might be a bunch of issues with the translation, since the project is made for everyone it is right that those who find errors in the translation and want to fix the issue must be able to do so

> [!NOTE] TODO:
> add a loading page
> add a check to see if the source or translation is less than 500 characters(it failed)
> make gunicorn print requests
> add logs

> [!CAUTION] Important Notice
> This repository is open-source under the GPL 3.0 license, but that applies **only to the code**.
> The translated text of *Reverend Insanity* included or produced by this project is **unauthorized and copyrighted** by the original author and publisher. 
> This project **does not grant permission** to redistribute or commercialize these translations.
