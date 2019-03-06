#!/usr/bin/env python3

import argparse
import configparser
import importlib
import logging
import sys
import time

import synbiohub_adapter as sbha

import sd2.metric

S_SYNBIOHUB = 'synbiohub'
O_URL = 'url'
O_USER = 'user'
O_PASSWORD = 'password'


class RiboswitchesMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def design_riboswitches(self):
        return self._query.query_design_riboswitches(pretty=True)

    @property
    def experiment_riboswitches(self):
        return self._query.query_experiment_riboswitches(by_sample=False)

    def fetch(self):
        result = []
        timestamp = time.time()
        dc = len(self.design_riboswitches)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Design Riboswitches',
                                          value=dc))
        ec = len(self.experiment_riboswitches)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Riboswitches',
                                          value=ec))
        return result


class PlasmidsMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def design_plasmids(self):
        return self._query.query_design_plasmids(pretty=True)

    @property
    def experiment_plasmids(self):
        return self._query.query_experiment_plasmids(by_sample=False)

    def fetch(self):
        result = []
        timestamp = time.time()
        dc = len(self.design_plasmids)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Design Plasmids',
                                          value=dc))
        ec = len(self.experiment_plasmids)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Plasmids',
                                          value=ec))
        return result


class GatesMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def design_gates(self):
        return self._query.query_design_gates(pretty=True)

    @property
    def experiment_gates(self):
        return self._query.query_experiment_gates(by_sample=False)

    def fetch(self):
        result = []
        timestamp = time.time()
        dc = len(self.design_gates)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Design Gates',
                                          value=dc))
        ec = len(self.experiment_gates)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Gates',
                                          value=ec))
        return result


class MediaMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def design_media(self):
        return self._query.query_design_media(pretty=True)

    @property
    def experiment_media(self):
        return self._query.query_experiment_media(by_sample=False)

    def fetch(self):
        result = []
        timestamp = time.time()
        dc = len(self.design_media)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Design Media',
                                          value=dc))
        ec = len(self.experiment_media)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Media',
                                          value=ec))
        return result


class ControlsMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def design_controls(self):
        return self._query.query_design_controls(pretty=True)

    @property
    def experiment_controls(self):
        return self._query.query_experiment_controls(by_sample=False)

    def fetch(self):
        result = []
        timestamp = time.time()
        dc = len(self.design_controls)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Design Controls',
                                          value=dc))
        ec = len(self.experiment_controls)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Controls',
                                          value=ec))
        return result


class PlansMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def experiment_plans(self):
        collections = [sbha.SD2Constants.SD2_EXPERIMENT_COLLECTION]
        rdf_type = 'http://sd2e.org#Experiment'
        plans = self._query.query_collection_members(collections=collections,
                                                     rdf_type=rdf_type)
        return self._query.format_query_result(plans, ['entity'])

    def fetch(self):
        result = []
        timestamp = time.time()
        ep = len(self.experiment_plans)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Experiment Plans',
                                          value=ep))
        return result


class TriplesMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def triples(self):
        sparql_query = 'SELECT (COUNT(?s) AS ?triples) WHERE { ?s ?p ?o }'
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        return self._query.format_query_result(result, ['triples'])

    def fetch(self):
        result = []
        timestamp = time.time()
        val = int(self.triples[0])
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Triples',
                                          value=val))
        return result


class PredicatesMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def predicates(self):
        sparql_query = '''SELECT ?p (COUNT(?p) as ?pCount)
          WHERE { ?s ?p ?o . }
          GROUP BY ?p
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        return self._query.format_query_result(result, ['p', 'pCount'])

    def fetch(self):
        result = []
        timestamp = time.time()
        val = len(self.predicates)
        result.append(sd2.metric.DataItem(timestamp=timestamp,
                                          name='Predicates',
                                          value=val))
        return result


class RelationsMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def predicates(self):
        sparql_query = '''SELECT ?o (COUNT(?o) as ?oCount)
          WHERE { ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o . }
          GROUP BY ?o
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        return self._query.format_query_result(result, ['o', 'oCount'])

    def fetch(self):
        result = []
        timestamp = time.time()
        for o in self.predicates:
            result.append(sd2.metric.DataItem(timestamp=timestamp,
                                              name=o['o'],
                                              value=int(o['oCount'])))
        return result


def collect_data(fetchers):
    fmt = '{ts},{name},{value}'
    for f in fetchers:
        data = f.fetch()
        for d in data:
            print(fmt.format(ts=int(d.timestamp),
                             name=d.name,
                             value=d.value))


def load_class(class_name):
    module_name = class_name[:class_name.rindex('.')]
    module = importlib.import_module(module_name)
    class_name = class_name[class_name.rindex('.') + 1:]
    cls = getattr(module, class_name)
    return cls


def instantiate_writer(metric_class, options=None):
    if options:
        return metric_class(options)
    else:
        return metric_class()


def load_writers(config, writers_section='writers'):
    result = []
    for option, value in config.items(writers_section):
        if config.has_section(value):
            msg = 'Loading {} from section {}'
            logging.info(msg.format(option, value))
            class_name = config.get(value, 'class')
            msg = 'Loading {} from class {}'
            logging.info(msg.format(value, class_name))
            cls = load_class(class_name)
            # Add other options from config to constructor call
            options = dict(config.items(value))
            instance = instantiate_writer(cls, options)
            result.append(instance)
        else:
            msg = 'Loading {} from class {}'
            logging.info(msg.format(option, value))
            cls = load_class(value)
            instance = instantiate_writer(cls)
            result.append(instance)
    return result


def instantiate_metric(metric_class, sbh_url, sbh_user=None,
                       sbh_password=None):
    instance = metric_class(sbh_url)
    if sbh_user and sbh_password:
        instance.login(sbh_user, sbh_password)
    return instance


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=argparse.FileType('r'),
                        metavar="CONFIG_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-u', '--sbh-user', metavar='SYNBIOHUB_USER')
    parser.add_argument('-p', '--sbh-password', metavar='SYNBIOHUB_PASSWORD')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    config = configparser.ConfigParser()
    config.read_file(args.config)

    if not config.has_section('metrics'):
        print('No "metrics" section found in {} configuration')
        sys.exit(1)

    sbh_url = config.get(S_SYNBIOHUB, O_URL,
                         fallback=sbha.SD2Constants.SD2_SERVER)
    sbh_user = args.sbh_user
    if not sbh_user:
        sbh_user = config.get(S_SYNBIOHUB, O_USER, fallback=None)
    sbh_password = args.sbh_password
    if not sbh_password:
        sbh_password = config.get(S_SYNBIOHUB, O_PASSWORD, fallback=None)

    metrics = []
    for option, value in config.items('metrics'):
        if config.has_section(value):
            msg = 'Loading {} from section {}'
            logging.info(msg.format(option, value))
            class_name = config.get(value, 'class')
            msg = 'Loading {} from class {}'
            logging.info(msg.format(value, class_name))
            cls = load_class(class_name)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, sbh_url, sbh_user, sbh_password)
            metrics.append(metric)
        else:
            msg = 'Loading {} from class {}'
            logging.info(msg.format(option, value))
            cls = load_class(value)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, sbh_url, sbh_user, sbh_password)
            metrics.append(metric)
    # results = [m.fetch() for m in metrics]
    results = []
    writers = load_writers(config)
    # writer = sd2.metric.api.DataMetricLogger()
    # csv_writer = sd2.metric.api.DataMetricCsvWriter()
    for m in metrics:
        logging.info('Fetching for {}'.format(type(m).__name__))
        items = m.fetch()
        for writer in writers:
            writer.write(m, items)


if __name__ == '__main__':
    main()
