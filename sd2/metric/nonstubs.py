
import collections
import time

from .api import DataMetric
from .api import DataItem

class NonStubsMetric(DataMetric):

    def __init__(self, url):
        super().__init__(url)

    # To find non-stubs by looking for modules or components that do
    # not have the stub_object predicate, see
    # http://www.townx.org/blog/elliot/describing-finding-subjects-which-dont-have-particular-predicate-sparql

    @property
    def modules_marked_nonstub(self):
        sparql_query = '''SELECT ?role, (COUNT(?role) as ?roleCount)
          WHERE {
              ?s <http://sd2e.org#stub_object> "false" .
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              ?s <http://sbols.org/v2#role> ?role
          }
          GROUP BY ?role
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['role', 'roleCount'])
        return result

    @property
    def modules_without_stub(self):
        sparql_query = '''SELECT ?role, (COUNT(?role) as ?roleCount)
          WHERE {
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              ?s <http://sbols.org/v2#role> ?role
              OPTIONAL { ?s <http://sd2e.org#stub_object> ?o } .
              FILTER (! bound(?o) )
          }
          GROUP BY ?role
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['role', 'roleCount'])
        return result

    @property
    def nonstub_modules(self):
        counts = collections.defaultdict(int)
        for row in self.modules_marked_nonstub:
            counts[row['role']] += int(row['roleCount'])
        for row in self.modules_without_stub:
            counts[row['role']] += int(row['roleCount'])
        return [(role, count) for role, count in counts.items()]

    def fetch(self):
        result = []
        timestamp = time.time()
        for (name, count) in self.nonstub_modules:
            name = '{:s}'.format(name)
            result.append(DataItem(timestamp=timestamp,
                                   name=name,
                                   value=count))

        return result
