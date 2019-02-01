import csv
import logging
import pathlib

import synbiohub_adapter as sbha


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
