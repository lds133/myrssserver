# My RSS grabber and proxy


## 1. Install venv

```
./makevenv.sh 
```

#### Debug 
```
source .venv/bin/activate
```


## 2. Run

```
cd server
```

```
.venv/bin/python runserver.py
```


#### Debug 
```
.venv/bin/python rssgrabber.py
```



## 3. Cloudflare

if tunnel named PAZ already exists


1.

```
cloudflared tunnel route dns PAZ rss
```

2.
edit config.yml in the  /etc/cloudflared  folder

```
...
    - hostname: rss.itmpaz2024.online
      service: http://localhost:33331
...
```


3.
```
sudo systemctl restart cloudflared
```

