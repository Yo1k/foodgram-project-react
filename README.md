# FoodGram

<a href="https://docs.python.org/3.8/">
<img src="https://img.shields.io/badge/Python-3.8-FFE873.svg?labelColor=4B8BBE" 
alt="Python requirement">
</a>

<a href="https://flake8.pycqa.org/en/5.0.4/">
<img src="https://img.shields.io/badge/flake8-5.0-E4D00A.svg?labelColor=555">
</a>

<a href="https://docs.pytest.org/en/6.2.x/contents.html">
<img src="https://img.shields.io/badge/pytest-6.2-E4D00A.svg?labelColor=555">
</a>

![workflow status](https://github.com/Yo1k/foodgram-project-react/actions/workflows/foodgram-workflow.yml/badge.svg)

## About
A web service with culinary recipes and an assistance to manage the necessary ingredients. The service allow to publish recipes, subscribe to publications of the other users, make your own list of favorite recipes, and create related list of ingredients, that necessary for cooking one or several chosen culinary dishes.

The service is deployed at: http://91.239.27.130/

Tech stack: \
[Django 3.2](https://docs.djangoproject.com/en/2.2/),
[Django REST framefowrk 3.12](https://www.django-rest-framework.org)


## Running the project in Docker

Clone this git repository. \
Set `./infra/.env` variables using as template `./infra/sample.env`.

Before starting, [install Docker Compose](https://docs.docker.com/compose/install/) if you do not have 
it. Below it is assumed that
[Docker's repositories](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
are set up. By default, the Docker daemon always runs as the `root` user. If you do not want to 
preface the docker command with `sudo` (or `su -`) see
[this](https://docs.docker.com/engine/install/linux-postinstall/). The following assumes that commands beginning with `#` are run as the `root` user. Start Docker daemon with command:

```shell
# service docker start
```
For further `docker compose` commands change directory to the `./infra` or add this fragment to entering commands: `docker compose -f ./infra/docker-compose.yaml <other_comands>`.

### Run containers

To create and run Docker containers run (`-d` to run services in the background):
```shell
# docker compose up -d
```
and to stop and delete containers:
```shell
# docker compose down -v
```

To find out `<CONTAINER ID>` of running containers run:
```shell
# docker container ls
```

### Setup web-service database and other files in containers

After starting the container you need to make migrations inside a container with `web` service:

```shell
# docker compose exec web python manage.py migrate
```

To create superuser:
```shell
# docker compose exec web python manage.py createsuperuser
```

To create folder with all Django static files:
```shell
# docker compose exec web python manage.py collectstatic --no-input 
```

To make database backups of the project running in the Docker use:
```shell
# docker compose exec web python manage.py dumpdata > ./data/<name backup>.json
```
`./infra/data/` &mdash; is dedicated folder for database backups and default data. Files in this folder are persistent regardless of whether docker containers are running or shut down.

To restore database from backup files run:
```shell
# docker compose exec web python manage.py loaddata ./data/<name backup>.json
```


## Endpoints

Documentation of endpoints is placed in file
`./docs/redoc.yaml `
To watch it in convenient way you can view it on `/api/docs/` endpoint after 
run the service or import yaml file to
[swagger editor](https://editor.swagger.io/) online resource.
