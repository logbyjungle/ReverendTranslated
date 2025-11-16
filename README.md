# ReverendTranslated

<p align="center">
    <img src="static/icon.png" alt="Perseverance" width="200">
</p>
<p align="center">
    <i>The translation is not perfect of course, but it is for sure better than those MTL sites</i><br>
    <i>The version of RI that is translated is in english, instead of the original chinese version, this might cause a further loss in meaning</i><br>
    <i>Thats why i'll be trying to add an option to choose which version to base the translation on</i><br>
</p>

---

## In order to be run locally you just have to:
```sh
git clone https://github.com/logbyjungle/ReverendTranslated.git
cd ReverendTranslated
pip install -m requirements.txt # use a venv if you want to
python main.py
```
and then enter the site at `localhost:5000`  

## If you instead want to host it for others you have to:  
- make sure you are not under **NAT**  
- `git clone https://github.com/logbyjungle/ReverendTranslated.git`  
- `cd ReverendTranslated`  

- Use [Duckdns](https://www.duckdns.org) to get a static address  
- I advise setting up a script in the host machine to update the public ip for Duckdns  
- make a `.env` file and put these info in this following format:  
```sh
DOMAIN=yourdomain.com
TZ=Europe/Rome
TOKEN=yourduckdnstoken
EMAIL=youremail@gmail.com # its required apparently
```
- `docker compose up -d --build --scale flask-app=NUMBEROFWORKERS` Use Docker Compose instead of normal Docker  
- both the `docker-compose.yml` and `.env` files can be deleted once it finishes building and running the containers  
- Port forward ports **80(http) and 443(https)**, remember to make your **ipv4** address static  

### If you also want to make everything more secure you have to use **https**:  
- go inside the shell of the nginx container and run `activate_https.sh`  
In case you dont intend to use Duckdns here is the content of the script, just modify the certbot part  
```sh
certbot certonly --non-interactive --agree-tos --email "$EMAIL" --preferred-challenges dns --authenticator dns-duckdns --dns-duckdns-token "$TOKEN" --dns-duckdns-propagation-seconds 60 -d "$DOMAIN"
cd etc/nginx/conf.d/
mv nginx.conf nginx.conf.disabled
mv nginx.conf.https nginx.conf
nginx -s reload
```  
The certificates can be managed in the `etc` folder, in case you want to use another location you can change this line in the `docker-compose.yml`:  
```
- ./etc/letsencrypt:/etc/letsencrypt
```

---

### You've noticed a translation problem and wish to fix it?  
Go to the `chapters` branch of the repository and look for a file with the same name of the id of your language  
If there is none create it  
Write into it with this following format  
```
Pattern
Replacement
---
```
Every `Pattern` is a python regex pattern, every `Replacement` is the text you want to replace the pattern with  
Multiple patterns can be inserted, just make sure there is a `---` to separate them  

---

This is a site hosted utilizing flask, it takes pages of RI's chapters from other sites and translate them by using google translate via selenium  

The objective to be reached is spreading *Gu Zhen Ren*'s work across the globe by making sure everyone can read it  

> ***TODO***  
> implement github actions: deploy containers and tests if requests work  
> implement security features: protection from ddos,fail2ban,modsecurity...  
> add github badges  
> make it possible to get translation from the original chinese version  
> translate the languages in language selection menu to their own language  
> add multiprocessing to translation  
> add logs  
> make the whole thing not just for reverend insanity only  
> delete translated chapters stored in cache for some reason  
> make it so that if memory is full then it `rm -rf`s the translations  
> when the text is loading give it a default value of a loading wheel gif + a lot of \n so that the bottom bar isnt shown  
> add hotkeys to navigate chapters  
