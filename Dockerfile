# Dockerfile to create the OpenGA Docker Image
FROM ubuntu:16.04
RUN apt-get -y update && apt-get install -y \
	libboost-system-dev \
	python \
        python-matplotlib

