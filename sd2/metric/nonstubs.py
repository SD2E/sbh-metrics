
import collections
import logging
import time

from .api import DataMetric

class NonStubsMetric(DataMetric):

    def __init__(self, url):
        super().__init__(url)

    @property
    def nonstub_modules(self):
        # Could stubs be marked with #stub_object = "false"? If so, adjust the filter
        sparql_query = '''SELECT ?s, ?role
          WHERE {
              ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              ?s <http://sbols.org/v2#role> ?role
              OPTIONAL { ?s <http://sd2e.org#stub_object> ?o } .
              FILTER (! bound(?o) && ! strstarts(str(?role), "http://www.openmath.org/cd/logic1"))
          }
          GROUP BY ?role
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['s', 'role'])
        return result

    def module_is_filled(self, sd2_name, sd2_type):
        sparql_query = '''SELECT ?rel
          WHERE {
              <%s> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              <%s> <http://sbols.org/v2#role> <%s> .
              <%s> ?rel ?o
              FILTER ( strstarts(str(?rel), "http://sbols.org/v2"))
          }
          GROUP BY ?type
        '''
        sparql_query = sparql_query % (sd2_name, sd2_name, sd2_type, sd2_name)
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        relations = self._query.format_query_result(result, ['rel'])
        for relation in relations:
            if relation.startswith('http://sbols.org/v2'):
                pass
            else:
                logging.info('Skipping %s', relation)
        return ('http://sbols.org/v2#module' in relations or
                'http://sbols.org/v2#interaction' in relations or
                'http://sbols.org/v2#functionalComponent' in relations)
        return filled_count, empty_count

    def fetch(self):
        result = []
        timestamp = int(time.time())
        count_by_type = collections.defaultdict(int)
        filled_by_type = collections.defaultdict(int)
        for row in self.nonstub_modules:
            sd2_name = row['s']
            sd2_type = row['role']
            count_by_type[sd2_type] += 1
            if self.module_is_filled(sd2_name, sd2_type):
                filled_by_type[sd2_type] += 1

        # Add the CSV header
        result.append(['Timestamp', 'URI', 'All', 'Filled', 'Empty'])
        for sd2_type, count in count_by_type.items():
            filled = filled_by_type[sd2_type]
            empty = count - filled
            result.append([timestamp, sd2_type, count, filled, empty])

        return result
