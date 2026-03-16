# ReverendTranslated

<p align="center">
    <img src="static/icon.png" alt="Perseverance" width="200">
</p>
<p align="center">
    <i>The translation is not perfect of course, but it is for sure better than those MTL sites</i><br>
    <i>The version of RI that is translated is in english, instead of the original chinese version, this might cause a further loss in meaning</i><br>
    <i>Thats why i'll be trying to add an option to choose which version to base the translation on</i><br>
</p>

![Build](https://github.com/logbyjungle/ReverendTranslated/actions/workflows/docker-image.yml/badge.svg)

---

## In order to be run locally you just have to:
```sh
git clone https://github.com/logbyjungle/ReverendTranslated.git
cd ReverendTranslated
pip install -m requirements.txt # use a venv if you want to
python main.py
```
And then enter the site at `localhost:5000`  
If it doesn't work you can build the try `Dockerfile`  

## If you instead want to host it for others you have to:  
fork the repository  
clone the `tunnel` branch  
add your github info to the `.env` file with this format:  
```
USERNAME=example
USEREMAIL=example@example.example
GITTOKEN=example
```
`COMPOSE_PROFILES=workers docker compose up -d --build --scale more-flask=HOWMANYEXTRAWORKERSYOUWANT`  

!!this readme is not finished yet!!  
also add github workflows test  
