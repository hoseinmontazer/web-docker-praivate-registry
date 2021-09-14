# Docker Private Registry UI
this is a django app for priavate docker registry frontend 


## Overview
This project  provide a simple user interface for your private docker registry , show image , tag , delete!!! 

## Features

-   list all your repositories/images.
-   list all tags for a image.
-   display image size
-   show `docker pull` for image
-   Show sha256 for specific tag
-   delete image with specific tag

## how  delete image

For deleting images, you need to activate the delete feature in your registry:

```yml
storage:
    delete:
      enabled: true
```
And you need to  run below command on registry this is the process of removing blobs from the filesystem
```sh
bin/registry garbage-collect  /etc/docker/registry/config.yml
```

## how  to run 
For useing  this repo  you can  pull **hoseinmontazer/web-docker-praivate-registry:1.0.0** iamge and create docker container 
```
docker run   -p 8000:8000  hoseinmontazer/web-docker-praivate-registry:1.0.0
```
