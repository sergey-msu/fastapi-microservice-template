# ExampleApp: Auth microservice

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
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

or (the last line)

```
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8001
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

## Docker
local:
```
cd src/auth
sudo docker build .
sudo docker images
sudo docker run -d -p 8001:8001 [image]
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
sudo -E docker-compose build
sudo -E docker-compose up
```

clear all (containers and images):
```
sudo docker container prune
sudo docker system prune -a
sudo docker volume ls
sudo docker volume rm [volume_name]
```

who is using port 80:
```
sudo lsof -i -P -n | grep 80
```

## tmux

start new session:
```
tmux new -s exampleapp-auth
```

detach from session:
CTRL+B,D

attach to session:
```
tmux a -t exampleapp-auth
```

## nginx

address already in use problem:
```
sudo netstat -plant | grep 80
sudo systemctl stop apache2
sudo systemctl stop postgresql
sudo systemctl stop mongodb.service
```
