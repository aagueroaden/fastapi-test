# fastapi-test repo, the salesforce_fastapi_adenuniversity_edu_pa 
this is a repo for the salesforce_fastapi proyect
It connects to salesforce and odoo mainly, but also has connections to google drive, facebook and mails

for the connection to salesforce, uses: `simple-salesforce`
for the connection to odoo, uses: `TODO`
for the connection to googledrive, uses: `googleapiclient`
for the connection to facebook, uses: `TODO`
for the connection to mails, uses: `TODO`

## Start the proyect in docker

Build the docker image

```sh
docker build -f [Dockerfile-file-that-you-want-to-build] -t [the-pod-name] [path/to/the/dockerfile]
```

Run the docker image
```sh
docker run -it -p [9000:9000] [the-pod-name] -e [ENV_VARIABLE_NAME]=[ENV_VARIABLE_VALUE]
```

ports `9000` are in the proyect itself, if you change it to another, use that port instead, but change the  env variable `APP_PORT`.

you need to add a `-e` for each env variable

## Start your proyect in docker-compose

build and run the docker-compose
```sh
docker-compose -f [Docker-compose-file.yml] up -d --build
```
`docker-compose-file.test.yml` start with the credentials of `test`
`docker-compose-file.prod.yml` start with the credentials of `prod`

## Local
export all enviroment variables to your terminal or shell

in a virtual enviroment in python3.10,

install requirements
```sh
pip3 install -r requirements.txt
```
run
```sh
python3 main.py
```

## Test

TODO, WANT TO USE `pytest`

## Documentation

TODO
