# Installation for Ubuntu or Debian systems

## Common section
```
apt install python3 python3-pip python-virtualenv git nginx uwsgi uwsgi-plugin-python3 redis-server
useradd -m -g www-data drapo
```
Create file '/etc/docker/daemon.json' if not exist
Add to damon.json: `{"insecure-registries":["<registry_host>:5000"]}`
with valid docker http-registry host and port. It must be ready to work
Read about registry: https://docs.docker.com/registry/

Then, restart the docker service with `systemctl restart docker`

```
usermod -aG docker drapo
su drapo
```

Follow commands need to be run as 'drapo' user
```
cd ~
git clone https://github.com/werelaxe/drapo.git
```

Create and active virtual environment

```
virtualenv -p /usr/local/bin/python3.7 venv
source venv/bin/activate
cd drapo/src/deploy
```

Install requirements

`pip3 install -r requirements.txt`

`cd <service_home>`

Where *service_home* is `~/drapo/src/deploy/builder` for builder and `~/drapo/src/deploy/deployer` for deployer.

For every service add service registry parameters in settings.py.

Create database with necessary stuff:
`./manage.py migrate`

Run main server:
`./manage.py runserver`

In another console (venv is necessary) run celery worker:
`./run-celery-worker.sh`
