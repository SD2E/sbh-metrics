import csv
import datetime
import logging
import pathlib
import requests
import re
from pprint import pprint
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry

import synbiohub_adapter as sbha

DATAFRAME_VERSION = '1.0.0'


class DataItem():

    def __init__(self, timestamp=0, name='', value=None):
        self.timestamp = timestamp
        self.name = name
        self.value = value

    def __iter__(self):
        # Nothing fancy, just yield the fields in order
        yield int(self.timestamp)
        yield self.name
        yield self.value


class DataMetric():

    def __init__(self, url):
        self._url = url
        self._query = sbha.SynBioHubQuery(url)

    def login(self, user, password):
        """Authenticate the connection to SynBioHub.
        This must be done prior to running any queries.
        """
        self._query.login(user, password)


class DataMetricWriter:

    def __init__(self):
        pass

    def fqcn(self, o):
        module = o.__class__.__module__
        class_name = o.__class__.__qualname__
        if module is None or module == str.__class__.__module__:
            return class_name
        else:
            return f'{module}.{class_name}'


class DataMetricLogger(DataMetricWriter):

    def __init__(self, logger=logging.getLogger()):
        # super().__init__()
        self.logger = logger

    def write(self, metric, items):
        pretty_class = metric.__class__.__name__
        for item in items:
            self.logger.info(f'{pretty_class} {item.name}: {item.value}')


class DataMetricCsvWriter(DataMetricWriter):

    def __init__(self, options):
        # super().__init__()
        self.out_dir = pathlib.Path('.')
        if 'out_dir' in options:
            self.out_dir = pathlib.Path(options['out_dir'])

    def _initialize_dir(self, dir_path):
        dir_path.mkdir(parents=True, exist_ok=True)

    def _initialize_file(self, path):
        if not path.exists():
            path.touch()
        # We may want to initialize the CSV header here as well

    def write(self, metric, items):
        self._initialize_dir(self.out_dir)
        pretty_class = metric.__class__.__name__
        csv_file = '{}.csv'.format(pretty_class)
        csv_path = self.out_dir / csv_file
        logging.info('CSV file name: {}'.format(str(csv_path)))
        self._initialize_file(csv_path)
        with csv_path.open('a') as fp:
            writer = csv.writer(fp)
            writer.writerows(items)


class DataMetricLogstashWriter(DataMetricWriter):
    def __init__(self, options):
        for param in ('url', 'key', 'secret'):
            setattr(self, param, options.get(param, None))

    def write(self, metric, items):
        pretty_class = metric.__class__.__name__
        logging.info('Stashing class: {}'.format(pretty_class))
        for item in items:
            msg = object_as_dict(item)
            # Allow filtering on  pretty_class in ElasticSearch
            msg['class'] = pretty_class
            # Lets us version the records in Elasticsearch
            msg['version'] = DATAFRAME_VERSION

            logging.info('URI: {}'.format(self.url))
            logging.info(f'Message: {msg}')
            try:
                r = requests.Session()
                # In case the Logstash HTTP endpoint gets overwhelmed
                retries = Retry(total=5, backoff_factor=1,
                                status_forcelist=[502, 503, 504])
                r.mount('https://', HTTPAdapter(max_retries=retries))
                r.post(self.url, json=msg, auth=HTTPBasicAuth(
                    self.key, self.secret))
                # r.raise_for_status()
            except Exception:
                logging.exception(
                    'Failed to POST payload to Logstash')
                raise


def object_as_dict(python_obj):
    """Transforms a metrics "item" into a dict representation for
    sending to HTTPxJSON Logstash
    """
    new_dict = {}
    for p in dir(python_obj):
        val = getattr(python_obj, p)
        # Ignore Nones, private methods, and anything with a sub-dict
        if isinstance(val, (list, tuple, str, int, float, bool)):
            if val is not None and not p.startswith('__'):
                if not hasattr(val, '__dict__'):
                    new_dict[p] = val
    # Make HTTPxJSON/Elasticsearch-friendly
    if 'timestamp' in new_dict:
        # Works w/ Elasticsearch mapping to read timestamp => @timestamp
        new_dict['timestamp'] = datetime.datetime.utcfromtimestamp(
            new_dict['timestamp']).isoformat() + 'Z'
    if 'name' in new_dict:
        new_dict['name'] = new_dict['name'].replace(' ', '-')

    return new_dict
