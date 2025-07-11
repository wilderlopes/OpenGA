# Dockerfile to create the OpenGA Docker Image
FROM ubuntu:16.04
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y update && apt-get install -y \
	libboost-all-dev \
	python3 \
    python3-pip \
    python3-numpy \
    python3-matplotlib \
    build-essential \
    libpcl-dev \
    pcl-tools \
    libflann-dev \
    cmake \
    vim \
    wget

