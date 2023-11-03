# fastapi-test repo
this is a repo for the salesforce_fastapi proyect

## Start the proyect in docker

Build the docker image

```sh
docker build -f [Dockerfile-file-that-you-want-to-build] -t [the-pod-name] [path/to/the/dockerfile]
```

Run the docker image
```sh
docker run -it -p [9000:9000] [the-pod-name]
```

ports 9000 are in the proyect itself, if you change it to another, use that port instead, but change the dockerfile and env variables also

## Local

in a virtual enviroment,

install requirements
```sh
pip3 install -r requirements.txt
```
run
```sh
python3 main.py -e [enviroment]
```

## Test

TODO

## Documentation

TODO
