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

## If you instead want to host it for others you have to:  
- make sure you are not under **NAT**  
- `git clone https://github.com/logbyjungle/ReverendTranslated.git`  
- `cd ReverendTranslated`  

- Use [Duckdns](https://www.duckdns.org) to get a static address  
- I advise setting up a script in the host machine to update the public ip for Duckdns  
- Make a `.env` file and put these info in this following format:  
```sh
DOMAIN=yourdomain.com
TZ=Europe/Rome
TOKEN=yourduckdnstoken
EMAIL=youremail@gmail.com # its required apparently
```
- `docker compose up -d --build`  
- If you want to add more workers then use this instead:  
`COMPOSE_PROFILES=workers docker compose up -d --build --scale more-flask=2`  
    *This for example adds 2 more workers*  
- Both the `docker-compose.yml` and `.env` files can be deleted once it finishes building and is running the containers  
- Port forward ports **80(http) and 443(https)**, remember to make your **ipv4** address static  

### If you also want to make everything more secure you have to use **https**:  
- Go inside the shell of the nginx container and run `activate_https.sh`  
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

> [!info] You've noticed a translation problem and wish to fix it?  
> Check out the `chapters` branch  

This is a site hosted utilizing flask, it takes pages of RI's chapters from other sites and translate them by using google translate via selenium  

The objective to be reached is spreading *Gu Zhen Ren*'s work across the globe by making sure everyone can read it  

> ***TODO***  
> implement security features: protection from ddos,fail2ban,modsecurity...  
> make it possible to get translation from the original chinese version  
> translate the languages in language selection menu to their own language  
> add multiprocessing to translation  
> add logs  
> make the whole thing not just for reverend insanity only  
> delete translated chapters stored in volumes at startup  
> make it so that if memory is full then it `rm -rf`s the translations  
> when the text is loading give it a default value of a loading wheel gif + a lot of \n so that the bottom bar isnt shown  
> add hotkeys to navigate chapters  
> check if the program is run correctly even if it is run from another directory  
> replace multiple containers with multiple workers  
> add a worker only to load the template of the page  
> add test to check if chapters are correctly translated  
> add test to check if the pattern is correct when making a PR to chapters branch  
