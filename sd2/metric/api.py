import logging

import synbiohub_adapter as sbha


class DataItem():

    def __init__(self, timestamp=0, name='', value=None):
        self.timestamp = timestamp
        self.name = name
        self.value = value


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

    def write_data_item(self, metric, item):
        pretty_class = metric.__class__.__name__
        self.logger.info(f'{pretty_class} {item.name}: {item.value}')
