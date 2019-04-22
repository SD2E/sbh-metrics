# Storing in ElasticSearch

The `DataMetricLogstashWriter` class serializes *Metrics records as JSON and
sends them over HTTPS to a Logstash pipeline (documented below), where
they are indexed into different ElasticSearch index depending on the set of
fields associated with the record. The decision of which index to route
to is based on the originating object's  `pretty_class` in the pipeline's
`filter` section.

## Configuration

The `logstash_writer` configuration requires the URL (always HTTPS) plus a
key and secret. Ideally, the secret should be not committed to GitHub or other
public repository.

```
[writers]
csv = csv_writer
logstash = logstash_writer
; logging = sd2.metric.api.DataMetricLogger

[logstash_writer]
class = sd2.metric.api.DataMetricLogstashWriter
url = https://sbh.logger.tacc.cloud/
key = drZkQ5SgFXTzrARxJkvYkPpZ
secret = Ty44dt4wgFcGT3uh9ppKn3vr
```

## Logstash Pipeline

This is the current configuration of the Logstash pipeline used to route
records to ElasticSearch indexes. It should be apparent that if the essential
logic of the `sd2.metric` classes changes, this filter will need to be
updated as well.

```
input {
    http {
        host => "0.0.0.0" # default: 0.0.0.0
        port => 31310 # default: 8080
        user => "NwJbaAMJyhaBFF8R4nyUK9ny"
        password => "qsCk4GDG2ukEK5tQs24crxfB"
        id => "json.sbh.input"
    }
}

filter {
    if [class] == 'StubsMetric' {
        clone {
            clones => [ "stubsmetric" ] # Clone the event
            add_field => { "[@metadata][stubsmetric]" => true }
        }
    } else {
         clone {
            clones => [ "datametric" ] # Clone the event
            add_field => { "[@metadata][datametric]" => true }
        }
    }
}
## Add your filters / logstash plugins configuration here
output {

    if [@metadata][stubsmetric] == "true" {
        elasticsearch {
            hosts => "elasticsearch:9200"
            index => "sbh-metrics-stubsmetric"
            id => "json.sbh.to_es.stubsmetric"
        }
    } else {
        if [@metadata][datametric] == "true" {
            elasticsearch {
                hosts => "elasticsearch:9200"
                index => "sbh-metrics-datametric"
                id => "json.sbh.to_es.datametric"
            }
        }
    }

    file {
        path => "/var/log/logstash/synbiohub.log"
        create_if_deleted => true
        id => "json.sbh.to_file.allmetrics"

    }
}
```

## Loading data from CSV

1. Ensure the **url**, **key**, and **secret** are set in the  `logstash_writer` section of the config.ini file.
2. Load a CSV file from disk as follows:

```shell
$ python sbh-metrics-loader.py config.ini ControlsMetric.csv --token
Token: 47e1f689
04/22/2019 12:28:34 INFO Loading ControlsMetric
04/22/2019 12:28:34 INFO Using pre-defined fieldnames
...
```

**WARNING** No de-duplication is implemented, so if a CSV file is accidentally
double-loaded into Logstash, the resulting records will need to be deleted by
hand from within the Kibana interface. This is helped substantially if the
CSV loads are done with the `--token` flag set for one `sbh-metrics-loader.py`,
which appends a time-based string token (generated at the start of execution)
to each Logstash record.
