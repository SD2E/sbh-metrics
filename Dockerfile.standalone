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

ADD sbh-metrics.py /sbh-metrics.py
ADD sd2 /sd2

ENTRYPOINT ["python3", "/sbh-metrics.py"]
CMD ["--help"]
