# SD2 SynBioHub Metrics

This directory contains a framework for gathering statistics or
metrics from a SynBioHub instance.

## Dependencies

This software requires
[synbiohub_adapter](https://github.com/SD2E/synbiohub_adapter), which
in turn requires the following:

* libxslt
* python3

See the `Dockerfile` for an example of installing the dependencies on Ubuntu 18 Bionic.

## Running

Execute the code like this:

```
python3 testing.py testing.ini
```

You should see results like this:

```
11/06/2018 15:12:41 INFO Loading riboswitches from class testing.RiboswitchesMetric
11/06/2018 15:12:41 INFO Loading plasmids from class testing.PlasmidsMetric
11/06/2018 15:12:41 INFO Loading gates from class testing.GatesMetric
11/06/2018 15:12:41 INFO Loading media from class testing.MediaMetric
11/06/2018 15:12:41 INFO Loading controls from section controls_metric
11/06/2018 15:12:41 INFO Loading controls_metric from class testing.ControlsMetric
.
.
.
```


## Docker

This directory includes a `Dockerfile` to build a docker image based
on Ubuntu 18 Bionic. The resulting image will have the SD1 SynBioHub
Metrics softwared included.

To build a docker image in this directory:

```
docker build --tag sd2e/sbh-metrics:0.2 .
```

To run the resulting image interactively:

```
docker run -it --rm --entrypoint /bin/bash sd2e/sbh-metrics:0.2
```

An example run from within the docker image:

```
root@e60eecff88b1:/# python3 /testing.py /testing.ini
11/06/2018 15:12:41 INFO Loading riboswitches from class testing.RiboswitchesMetric
11/06/2018 15:12:41 INFO Loading plasmids from class testing.PlasmidsMetric
11/06/2018 15:12:41 INFO Loading gates from class testing.GatesMetric
11/06/2018 15:12:41 INFO Loading media from class testing.MediaMetric
11/06/2018 15:12:41 INFO Loading controls from section controls_metric
11/06/2018 15:12:41 INFO Loading controls_metric from class testing.ControlsMetric
11/06/2018 15:12:41 INFO Loading plans from class testing.PlansMetric
11/06/2018 15:12:41 INFO Loading csv from section csv_writer
11/06/2018 15:12:41 INFO Loading csv_writer from class sd2.metric.api.DataMetricCsvWriter
11/06/2018 15:12:41 INFO Loading logging from class sd2.metric.api.DataMetricLogger
11/06/2018 15:12:41 INFO Fetching for RiboswitchesMetric
11/06/2018 15:12:48 INFO CSV file name: /tmp/test_csv_writer/RiboswitchesMetric.csv
11/06/2018 15:12:48 INFO RiboswitchesMetric Design Riboswitches: 193
11/06/2018 15:12:48 INFO RiboswitchesMetric Experiment Riboswitches: 0
11/06/2018 15:12:48 INFO Fetching for PlasmidsMetric
11/06/2018 15:12:49 INFO CSV file name: /tmp/test_csv_writer/PlasmidsMetric.csv
11/06/2018 15:12:49 INFO PlasmidsMetric Design Plasmids: 30
11/06/2018 15:12:49 INFO PlasmidsMetric Experiment Plasmids: 28
11/06/2018 15:12:49 INFO Fetching for GatesMetric
11/06/2018 15:12:51 INFO CSV file name: /tmp/test_csv_writer/GatesMetric.csv
11/06/2018 15:12:51 INFO GatesMetric Design Gates: 48
11/06/2018 15:12:51 INFO GatesMetric Experiment Gates: 48
11/06/2018 15:12:51 INFO Fetching for MediaMetric
11/06/2018 15:12:52 INFO CSV file name: /tmp/test_csv_writer/MediaMetric.csv
11/06/2018 15:12:52 INFO MediaMetric Design Media: 37
11/06/2018 15:12:52 INFO MediaMetric Experiment Media: 9
11/06/2018 15:12:52 INFO Fetching for ControlsMetric
11/06/2018 15:12:53 INFO CSV file name: /tmp/test_csv_writer/ControlsMetric.csv
11/06/2018 15:12:53 INFO ControlsMetric Design Controls: 20
11/06/2018 15:12:53 INFO ControlsMetric Experiment Controls: 18
11/06/2018 15:12:53 INFO Fetching for PlansMetric
11/06/2018 15:12:54 INFO CSV file name: /tmp/test_csv_writer/PlansMetric.csv
11/06/2018 15:12:54 INFO PlansMetric Experiment Plans: 55
```

# Running from cron

To run the image via a cron job, create an entry like this:

```
# m h  dom mon dow   command
0 1 * * * docker run --rm -v /path/to/output/dir:/sd2metrics -v /path/to/config.ini:/config.ini sd2e/sbh-metrics:0.2 /config.ini > /path/to/log-file.log 2>&1
```

# Configuration in Docker

The configuration file can contain the SynBioHub password. In order to
safely communicate that information to the docker image, mount the
file when runnning docker. See the cron example for how to mount a
file when running a docker image.
