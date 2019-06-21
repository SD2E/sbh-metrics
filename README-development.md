# Development tips

## Run inside the docker image

It is easy to mount a directory into a docker container. This allows
files to be edited outside the container, and executed inside the
container.

1. Build the docker image

    ```
    docker build --tag tcmitchell/sbh-metrics-reactor:1.1 .
    ```

2. Run the docker image and mount the current directory into the running container

    ```
    docker run -v$(pwd):/sbh-metrics --rm -it --entrypoint /bin/bash tcmitchell/sbh-metrics-reactor:1.1
    ```

4. Set up an appropriate config file

    ```ini
    [metrics]
    bugged = sd2.metric.BuggedLinksMetric

    [writers]
    csv = csv_writer

    [csv_writer]
    class = sd2.metric.api.DataMetricCsvWriter
    out_dir = /sd2metrics

    [synbiohub]
    user = scott
    password = tiger
    ```

3. Run sbh-metrics inside the docker container

    ```
    cd /sbh-metrics
    
    python3 sbh-metrics.py metrics.ini
    
    ```
