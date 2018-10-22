#!/usr/bin/env python3

import argparse
import configparser
import importlib
import logging
import sys
import time

import synbiohub_adapter as sbha

import sd2.metric


class Statistics:

    def __init__(self, url):
        self._url = url
        self._query = sbha.SynBioHubQuery(url)

    @property
    def design_riboswitches(self):
        return self._query.query_design_riboswitches(pretty=True)

    @property
    def experiment_riboswitches(self):
        return self._query.query_experiment_riboswitches(by_sample=False)

    @property
    def design_plasmids(self):
        return self._query.query_design_plasmids(pretty=True)

    @property
    def experiment_plasmids(self):
        return self._query.query_experiment_plasmids(by_sample=False)

    @property
    def design_gates(self):
        return self._query.query_design_gates(pretty=True)

    @property
    def experiment_gates(self):
        return self._query.query_experiment_gates(by_sample=False)

    @property
    def design_media(self):
        return self._query.query_design_media(pretty=True)

    @property
    def experiment_media(self):
        return self._query.query_experiment_media(by_sample=False)

    @property
    def design_controls(self):
        return self._query.query_design_controls(pretty=True)

    @property
    def experiment_controls(self):
        return self._query.query_experiment_controls(by_sample=False)

    @property
    def experiment_plans(self):
        collections = [sbha.SD2Constants.SD2_EXPERIMENT_COLLECTION]
        rdf_type = 'http://sd2e.org#Experiment'
        plans = self._query.query_collection_members(collections=collections,
                                                     rdf_type=rdf_type)
        return self._query.format_query_result(plans, ['entity'])

    def report(self):
        design_riboswitches = self.design_riboswitches
        exp_riboswitches = self.experiment_riboswitches
        msg = '{:d} out of {:d} riboswitches'
        print(msg.format(len(exp_riboswitches), len(design_riboswitches)))
        design_plasmids = self.design_plasmids
        exp_plasmids = self.experiment_plasmids
        msg = '{:d} out of {:d} plasmids'
        print(msg.format(len(exp_plasmids), len(design_plasmids)))
        design_gates = self.design_gates
        exp_gates = self.experiment_gates
        msg = '{:d} out of {:d} gates'
        print(msg.format(len(exp_gates), len(design_gates)))
        design_media = self.design_media
        exp_media = self.experiment_media
        msg = '{:d} out of {:d} media'
        print(msg.format(len(exp_media), len(design_media)))
        design_controls = self.design_controls
        exp_controls = self.experiment_controls
        msg = '{:d} out of {:d} controls'
        print(msg.format(len(exp_controls), len(design_controls)))
        exp_plans = self.experiment_plans
        msg = '{:d} experiment plans'
        print(msg.format(len(exp_plans)))


# class DataItem():

#     def __init__(self, timestamp=0, name='', value=None):
#         self.timestamp = timestamp
#         self.name = name
#         self.value = value


# class DataMetric():

#     def __init__(self, url):
#         self._url = url
#         self._query = sbha.SynBioHubQuery(url)


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


def collect_data(fetchers):
    fmt = '{ts},{name},{value}'
    for f in fetchers:
        data = f.fetch()
        for d in data:
            print(fmt.format(ts=int(d.timestamp),
                             name=d.name,
                             value=d.value))


url = sbha.SD2Constants.SD2_SERVER
fetchers = [
    RiboswitchesMetric(url),
    PlasmidsMetric(url),
    GatesMetric(url),
    MediaMetric(url),
    ControlsMetric(url),
    PlansMetric(url)
]

# collect_data(fetchers)

# for i in range(2):
#     collect_data(fetchers)
#     time.sleep(60)


def load_metric(class_name):
    module_name = class_name[:class_name.rindex('.')]
    module = importlib.import_module(module_name)
    class_name = class_name[class_name.rindex('.') + 1:]
    cls = getattr(module, class_name)
    return cls


def instantiate_metric(metric_class, sbh_url):
    return metric_class(sbh_url)


def demonstrate(class_name):
    "A quick how to"
    c = load_metric(class_name)
    m = instantiate_metric(c, url)
    r = m.fetch()
    pr = [(d.name, d.value) for d in r]
    print(pr)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=argparse.FileType('r'),
                        metavar="CONFIG_FILE")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    config = configparser.ConfigParser()
    config.read_file(args.config)

    if not config.has_section('metrics'):
        print('No "metrics" section found in {} configuration')
        sys.exit(1)

    metrics = []
    for option, value in config.items('metrics'):
        if config.has_section(value):
            msg = 'Loading {} from section {}'
            logging.info(msg.format(option, value))
            class_name = config.get(value, 'class')
            msg = 'Loading {} from class {}'
            logging.info(msg.format(value, class_name))
            cls = load_metric(class_name)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, url)
            metrics.append(metric)
        else:
            msg = 'Loading {} from class {}'
            logging.info(msg.format(option, value))
            cls = load_metric(value)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, url)
            metrics.append(metric)
    # results = [m.fetch() for m in metrics]
    results = []
    for m in metrics:
        logging.info('Fetching for {}'.format(type(m).__name__))
        results.append(m.fetch())
    logging.debug('Results = {}'.format(results))
    for result in results:
        logging.debug('Result = {}'.format(result))
        for r in result:
            print('Metric {} = {}'.format(r.name, r.value))


if __name__ == '__main__':
    main(sys.argv)
