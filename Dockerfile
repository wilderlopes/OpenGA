# Dockerfile to create the OpenGA Docker Image
FROM ubuntu:16.04
RUN apt-get -y update && apt-get install -y \
	libboost-all-dev \
	python3 \
        python3-matplotlib \
	python3-numpy
        python3-pip

