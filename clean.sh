#!/bin/bash

docker stop daftie
docker rm daftie
docker rmi -f lotbs/daft
