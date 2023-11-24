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
docker run -it -p [9000:9000] [the-pod-name]
```

ports `9000` are in the proyect itself, if you change it to another, use that port instead, but change the dockerfile and env variables also

## Local

in a virtual enviroment in python3.10,

install requirements
```sh
pip3 install -r requirements.txt
```
run
```sh
python3 main.py -e [enviroment]
```

## Test

TODO, WANT TO USE `pytest`

## Documentation

TODO
