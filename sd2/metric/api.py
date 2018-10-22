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
