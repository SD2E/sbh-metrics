#!/usr/bin/env python3

import argparse
import configparser
import importlib
import logging
import sys
import time

import synbiohub_adapter as sbha

import sd2.metric


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


class StubsMetric(sd2.metric.DataMetric):

    def __init__(self, url):
        super().__init__(url)

    # To find non-stubs by looking for modules or components that do
    # not have the stub_object predicate, see
    # http://www.townx.org/blog/elliot/describing-finding-subjects-which-dont-have-particular-predicate-sparql

    @property
    def stub_modules(self):
        """Find all ModuleDefinitions that are marked as stubs. Count the
        stubs by ModuleDefinition.role. Return a list of tuples as
        [(role1, count1), (role2, count2) ... ]

        """
        sparql_query = '''SELECT ?role, (COUNT(?role) as ?roleCount)
          WHERE {
              ?s <http://sd2e.org#stub_object> "true" .
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              ?s <http://sbols.org/v2#role> ?role
          }
          GROUP BY ?role
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['role', 'roleCount'])
        return [(row['role'], int(row['roleCount'])) for row in result]

    @property
    def stub_components(self):
        """Find all ComponentDefinitions that are marked as stubs. Count the
        stubs by ComponentDefinition.type. Return a list of tuples as
        [(type1, count1), (type2, count2) ... ]

        """
        sparql_query = '''SELECT ?type, (COUNT(?type) as ?typeCount)
          WHERE {
              ?s <http://sd2e.org#stub_object> "true" .
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ComponentDefinition> .
              ?s <http://sbols.org/v2#type> ?type
          }
          GROUP BY ?type
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['type', 'typeCount'])
        return [(row['type'], int(row['typeCount'])) for row in result]

    @property
    def stubs(self):
        sparql_query = '''SELECT ?s, ?p, ?o
          WHERE {
              ?s <http://sd2e.org#stub_object> "true" .
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ComponentDefinition> .
              ?s ?p ?o
          }
          GROUP BY ?type
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        logging.debug('raw result: {}'.format(result))
        stubs = self._query.format_query_result(result, ['s', 'p', 'o'])
        sstubs = [(stub['s'], stub['p'], stub['o']) for stub in stubs]
        # sstubs.sort(key=lambda x: x[0])
        sstubs.sort()
        for stub in sstubs:
            logging.info('{}'.format(stub))
        return stubs

    @property
    def stubs_good(self):
        sparql_query = '''SELECT ?type, (COUNT(?type) as ?typeCount)
          WHERE {
              ?s <http://sd2e.org#stub_object> "true" .
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type
          }
          GROUP BY ?type
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        logging.info('raw result: {}'.format(result))
        stubs = self._query.format_query_result(result, ['type', 'typeCount'])
        return stubs

    @property
    def nonstubs(self):
        sparql_query = '''SELECT ?type, (COUNT(?type) as ?typeCount)
          WHERE {
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?type .
              MINUS { ?s <http://sd2e.org#stub_object> "true" }
          }
          GROUP BY ?type
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        stubs = self._query.format_query_result(result, ['type', 'typeCount'])
        return stubs

    def fetch(self):
        result = []
        timestamp = time.time()
        module_stub_counts = self.stub_modules
        for (role, role_count) in module_stub_counts:
            result.append(sd2.metric.DataItem(timestamp=timestamp,
                                              name=role,
                                              value=role_count))

        component_stub_counts = self.stub_components
        for (name, count) in component_stub_counts:
            result.append(sd2.metric.DataItem(timestamp=timestamp,
                                              name=name,
                                              value=count))
        # for stub in self.stubs:
        #     logging.info('Stub {}'.format(stub))
        #     result.append(sd2.metric.DataItem(timestamp=timestamp,
        #                                       name=stub['type'],
        #                                       value=stub['typeCount']))
        # for nonstub in self.nonstubs:
        #     result.append(sd2.metric.DataItem(timestamp=timestamp,
        #                                       name='Nonstub {}'.format(nonstub['type']),
        #                                       value=nonstub['typeCount']))
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


def instantiate_metric(metric_class, sbh_url):
    return metric_class(sbh_url)


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

    # Push the SynBioHub URL out to the config file
    url = sbha.SD2Constants.SD2_SERVER

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
            cls = load_class(class_name)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, url)
            metrics.append(metric)
        else:
            msg = 'Loading {} from class {}'
            logging.info(msg.format(option, value))
            cls = load_class(value)
            # Add other options from config to constructor call,
            # probably as a dictionary
            metric = instantiate_metric(cls, url)
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
        results.append(items)
    # logging.debug('Results = {}'.format(results))
    for result in results:
        # logging.debug('Result = {}'.format(result))
        for r in result:
            logging.debug('Metric {} = {}'.format(r.name, r.value))


if __name__ == '__main__':
    main(sys.argv)
