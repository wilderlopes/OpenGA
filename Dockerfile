# Dockerfile to create the OpenGA Docker Image
FROM ubuntu:14.04
RUN apt-get -y update && apt-get install -y \
	libboost-system1.54-dev \
	python \
        python-matplotlib

