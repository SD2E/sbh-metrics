FROM ubuntu:bionic

RUN apt-get -y update && \
    apt-get -y install \
      git \
      libxslt1-dev \
      python3 \
      python3-pip \
      && \
    apt-get clean

RUN pip3 install \
      --process-dependency-link \
      git+https://github.com/SD2E/synbiohub_adapter.git

ADD testing.py /testing.py
ADD testing.ini /testing.ini
ADD sd2 /sd2
