# docker

---
## install
* [install in mac](https://docs.docker.com/docker-for-mac/)
* [install in ubuntu](https://docs.docker.com/engine/installation/linux/ubuntulinux/)

### Requirements
#### For ubuntu
Docker has two important installation requirements:

* Docker only works on a 64-bit Linux installation.
* Docker requires version 3.10 or higher of the Linux kernel. 

```bash
$ uname -r
3.11.0-15-generic
```

---
## About Docker
[what is aufs](http://www.open-open.com/lib/view/open1440483391763.html)

---
## Commands
### version check:
```bash
$docker --version

$docker-machine --version

$docker-compose --version
```
### process check:
```bash
# list running docker process
$docker ps

# list all docker process
$docker ps -a
```
### examples:
#### hello world:
```bash
$docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c04b14da8d14: Pull complete 
Digest: sha256:0256e8a36e2070f7bf2d0b0763dbabdd67798512411de4cdcf9431a1feb60fd9
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker Hub account:
 https://hub.docker.com

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```
#### Dockerized web server
```bash
# -d --datch run docker process in background
# -p --publish-all Publish all exposed ports to random ports
# --name run process using the giving name
# run `docker run --help` for more information
$docker run -d -p 80:80 --name webserver nginx
CONTAINER ID        IMAGE               COMMAND
6ab6f0e2a66a        nginx               "nginx -g 'daemon off"   

CREATED             STATUS              PORTS 
27 minutes ago      Up 27 minutes     0.0.0.0:80->80/tcp, 443/tcp   

NAMES
webserver

# use file from local
$cd <path_to_here_and_there>/docker/
$mkdir site
$echo "hello, docker" > index.html

$docker run -d -P -v <path_to_here_and_there>/docker/site:/usr/share/nginx/html --name mysite nginx
$docker port mysite
443/tcp -> 0.0.0.0:32769
80/tcp -> 0.0.0.0:32770

$echo "docker is greate" > docker.html
# visit localhost:32770 to see what is happen
```
#### run ubuntu
```bash
$docker run ubuntu:14.04 /bin/echo 'Hello world'
Hello world

# -t --tty		Allocate a pseudo(fake)-TTY
# -i --interactive		Keep STDIN open even if not attached
$docker run -t -i ubuntu:14.04 /bin/bash
root@af8bae53bdd3:/# pwd
root@af8bae53bdd3:/# exit
```
### container operations
```bash
# run
$docker run hello-world
$docker run -d -p 80:80 --name webserver nginx
$docker run -d -P --name webserver nginx
$docker run -t -i ubuntu:14.04 /bin/bash
#-P 标识(flags)是 -p 5000 的缩写，它将会把容器内部的 5000 端口映射到本地 Docker 主机的高位端口上(这个端口的通常范围是 32768 至 61000)。我们也可以指定 -p 标识来绑定指定端口。-p 5000:5000 这将会把容器内部的 5000 端口映射到我们本地主机的 5000 端口上。

# stop use process's name
$docker stop webserver
$docker kill webserver
# stop use process's id
$docker stop 6ab6f0e2a66a
$docker kill 6ab6f0e2a66a

# check containers
$docker ps
$docker ps -a	#check all container
$docker ps -l	#check detail

# restart
$docker start container_name

# stop and remove a container
$docker rm -f webserver

# check ports container is using
$docker port container_name
$docker port container_name container_port
$docker port container_name 5000	# 5000 is the container's port 4000 is the local port 
4000

# check container's stdout
$docker logs container
$docker logs -f container #-f == tail -f

# check top process in container
$docker top container_name

# check contaienr's status and configurations
$docker inspect container_name
$docker inspect -f '{{ .NetworkSettings.IPAddress }}' contianer_name	#specify a field, like container's ip
172.17.0.5
```
### image operations

```bash
# list images
$docker images
REPOSITORY       TAG      IMAGE ID      CREATED      VIRTUAL SIZE
ubuntu           13.10    5e019ab7bf6d  4 weeks ago  180 MB

# pull a image from docker hub
$docker pull image_name
$docker pull user_name/image_name

# two ways to create a new image
# 1: modify image from docker hub
$docker pull training/sinatra
$docker run -t -i training/sinatra bin/bash
root@0b2616b0e5a8:/#gem install json
root@0b2616b0e5a8:/#exit
$docker images
REPOSITORY				IMAGE ID
ouruser/sinatra 		0b2616b0e5a8 
$docker commit -m='msg' -a='author' 0b2616b0e5a8 ouruser/sinatra:v2
$docker commit -m='msg' -a='author' IMG_ID [docker_user]/[image_name]:tag
# 2: create a new one use Dockerfile
# check <path_to_here_and_there>/docker/Dockerfile for an example
$docker build -t ouruser/sinatra:v2 .	# . is path to Dockerfile

# set a tag for a image
$docker tag IMG_ID ouruser/sinatra:devel	# devel is new tag's name
$docker images ouruser/sinatra	# check all ourser/sinatra images

# image digests
$docker images --digests | head
$docker pull ouruser/sinatra:DIGESTS

# push image to docker hub
$docker push ouruser/sinatra

# remove a image by image's name or image's id
$docker rmi image_name|image_id
```

## settings
While docker is running,there will be a whale in the status bar, like this:

![](https://docs.docker.com/docker-for-mac/images/whale-x.png)

You can change your docker settings use this whale  `·(>^ω^<)·`.
### preferences
