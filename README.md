# dzidzai
An e-Learning platform

Run memcached docker container:
```shell
docker run -it --rm --name memcached -p 11211:11211 memcached -m 64
```

Run Redis Docker container:
```shell
docker run -it --rm --name redis -p 6379:6379 redis
```