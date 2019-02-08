
import collections
import logging
import time

from .api import DataMetric


class ComponentDefinition:

    KEY_STUB = 'stub'
    KEY_SEQUENCE = 'sequence'
    KEY_COMPONENT = 'component'
    KEY_SEQUENCE_ANNOTATION = 'sequenceAnnotation'


class ModuleDefinition:

    KEY_STUB = 'stub'
    KEY_SUBTYPE = 'subtype'
    KEY_FUNCTIONAL_COMPONENT = 'functionalComponent'
    KEY_INTERACTION = 'interaction'
    KEY_MODULE = 'module'

    def __init__(self, db_values):
        # Should probably validate the values a bit
        self._db_values = db_values

    @property
    def subtype(self):
        return self._db_values[ModuleDefinition.KEY_SUBTYPE]

    def is_stub(self):
        return (ModuleDefinition.KEY_STUB in self._db_values and
                self._db_values[ModuleDefinition.KEY_STUB] == 'true')

    def is_filled(self):
        return (ModuleDefinition.KEY_FUNCTIONAL_COMPONENT in self._db_values or
                ModuleDefinition.KEY_INTERACTION in self._db_values or
                ModuleDefinition.KEY_MODULE in self._db_values)

    def is_empty(self):
        return not self.is_filled()


class SubTypeCounter:

    def __init__(self):
        self.subtype = None
        self.stubs = 0
        self.filled_stubs = 0
        self.empty_stubs = 0
        self.nonstubs = 0
        self.filled_nonstubs = 0
        self.empty_nonstubs = 0

    def add_component(self, thing):
        if self.subtype is None:
            self.subtype = thing.subtype
        if thing.is_stub():
            self.stubs += 1
            if thing.is_filled():
                self.filled_stubs += 1
            else:
                self.empty_stubs += 1
        else:
            self.nonstubs += 1
            if thing.is_filled():
                self.filled_nonstubs += 1
            else:
                self.empty_nonstubs += 1


class NonStubsMetric(DataMetric):

    def __init__(self, url):
        super().__init__(url)

    def get_modules(self):
        sparql_query = '''SELECT ?type ?subtype ?stub ?module ?interaction
                                 ?functionalComponent
          WHERE {
              ?type <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
              ?type <http://sbols.org/v2#role> ?subtype .
              OPTIONAL { ?type <http://sd2e.org#stub_object> ?stub }
              OPTIONAL { ?type <http://sbols.org/v2#module> ?module }
              OPTIONAL { ?type <http://sbols.org/v2#interaction> ?interaction }
              OPTIONAL { ?type <http://sbols.org/v2#functionalComponent> ?functionalComponent }
              FILTER (! strstarts(str(?subtype), "http://www.openmath.org/cd/logic1"))
          }
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result,
                                                 ['type', 'subtype', 'stub',
                                                  'module', 'interaction',
                                                  'functionalComponent'])
        logging.info('result type is %s', type(result))
        result = [ModuleDefinition(dbv) for dbv in result]
        return result

    @property
    def nonstub_modules(self):
        # Could stubs be marked with #stub_object = "false"? If so, adjust the filter
        sparql_query = '''SELECT ?s ?role
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
        modules = self.get_modules()

        rows = collections.defaultdict(SubTypeCounter)
        for m in modules:
            rows[m.subtype].add_component(m)

        for st in sorted(rows.keys()):
            row = rows[st]
            logging.info('%s, %s, %s, %s, %s, %s, %s',
                         st, row.stubs, row.filled_stubs, row.empty_stubs,
                         row.nonstubs, row.filled_nonstubs, row.empty_nonstubs)
        return []

    def fetch_old(self):
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
        # Don't write the header each time, it ends up as a row in the
        # middle when appending to the file.
        # result.append(['Timestamp', 'URI', 'All', 'Filled', 'Empty'])
        for sd2_type, count in count_by_type.items():
            filled = filled_by_type[sd2_type]
            empty = count - filled
            result.append([timestamp, sd2_type, count, filled, empty])

        return result
