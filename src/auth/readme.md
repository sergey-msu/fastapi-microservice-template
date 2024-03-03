# InvestApp: Auth microservice

## before the first start

```
cd src/auth
python -m venv venv
source venv/bin/activate
pip install -m requirements.txt
```

## regular local start

```
cd src/auth
source venv/bin/activate
export APP_MODE=[dev|prod]
export APP_SECRET_KEY=[GLOBAL_SECRET_KEY]
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

or (the last line)

```
gunicorn app:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8001
```

## run tests
```
cd src/auth
pytest
```

## run flake8
```
cd src/auth
flake8
```

## update secrets file

```
from cryptography.fernet import Fernet

secrets = {
    'AUTH_SECRET_KEY': 'sadsadsadsa',
}
secrets = str(secrets).encode()

key = '[APP_SECRET_KEY]'
encrypted_item = Fernet(key).encrypt(secrets)
print(encrypted_item)
```

## Docker
local:
```
cd src/auth
sudo docker build .
sudo docker images
sudo docker run -d \
    -e APP_SECRET_KEY=[dev|prod] \
    -e APP_SECRET_KEY=[GLOBAL_SECRET_KEY] \
    -e MONGO_PASSWORD=[MONGO_PASSWORD] \
    -p 8001:8001 [image]
```

working with http://0.0.0.0:8001/api/v1/docs :
```
sudo docker ps
sudo docker exec -ti [container] bash
sudo docker stop [container]
```

compose:
```
cd src/auth
export APP_SECRET_KEY=[GLOBAL_SECRET_KEY]
export APP_MODE=[APP_MODE]
export MONGO_PASSWORD=[MONGO_PASSWORD]
sudo -E docker-compose build
sudo -E docker-compose up
```

clear all (containers and images):
```
sudo docker container prune
sudo docker system prune -a
```

who is using port 80:
```
sudo lsof -i -P -n | grep 80
```

## tmux

start new session:
```
tmux new -s investapp-auth
```

detach from session:
CTRL+B,D

attach to session:
```
tmux a -t investapp-auth
```

## nginx

address already in use problem:
```
sudo netstat -plant | grep 80
sudo systemctl stop apache2
sudo systemctl stop postgresql
sudo systemctl stop mongodb.service
```
