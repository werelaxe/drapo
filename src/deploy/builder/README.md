# Installation for Ubuntu or Debian systems ***

`apt install python3 python3-pip python-virtualenv git nginx uwsgi uwsgi-plugin-python3 redis-server`

`useradd -m -g www-data drapo`
`usermod -aG docker drapo`
`su drapo`

Follow commands need to be run as 'drapo' user

`cd ~`

`git clone https://github.com/werelaxe/drapo.git`

Create and active virtual environment

```virtualenv -p /usr/local/bin/python3.7 venv`
source venv/bin/activate
cd drapo/src/deploy/builder```

Install requirements

`pip3 install -r requirements.txt`

Create file '/etc/docker/daemon.json' if not exist
Add to damon.json: `{"insecure-registries":["<registry_host>:<registry_port>"]}`
with valid docker http-registry host and port. It must be ready to work
Read about registry: https://docs.docker.com/registry/


# Running
Create database with necessary stuff:
`./manage.py migrate`

Run main server:
`./manage.py runserver`

In another console (venv is necessary) run celery worker:
`./run-celery-worker.sh`
