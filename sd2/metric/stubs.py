
import collections
import logging
import time

from .api import DataMetric


class BaseDefinition:

    KEY_STUB = 'stub'
    KEY_SUBTYPE = 'subtype'

    def __init__(self, db_values):
        # Should probably validate the values a bit
        self._db_values = db_values

    @property
    def subtype(self):
        return self._db_values[BaseDefinition.KEY_SUBTYPE]

    def is_stub(self):
        return (ModuleDefinition.KEY_STUB in self._db_values and
                self._db_values[BaseDefinition.KEY_STUB] == 'true')

    def is_filled(self):
        # This must be defined in derived classes
        raise NotImplementedError

    def is_empty(self):
        return not self.is_filled()


class ComponentDefinition(BaseDefinition):

    KEY_SEQUENCE = 'sequence'
    KEY_COMPONENT = 'component'
    KEY_SEQUENCE_ANNOTATION = 'sequenceAnnotation'

    def __init__(self, db_values):
        super().__init__(db_values)

    def is_filled(self):
        return (ComponentDefinition.KEY_COMPONENT in self._db_values or
                ComponentDefinition.KEY_SEQUENCE in self._db_values or
                ComponentDefinition.KEY_SEQUENCE_ANNOTATION in self._db_values)


class ModuleDefinition(BaseDefinition):

    KEY_FUNCTIONAL_COMPONENT = 'functionalComponent'
    KEY_INTERACTION = 'interaction'
    KEY_MODULE = 'module'

    def __init__(self, db_values):
        super().__init__(db_values)

    def is_filled(self):
        return (ModuleDefinition.KEY_FUNCTIONAL_COMPONENT in self._db_values or
                ModuleDefinition.KEY_INTERACTION in self._db_values or
                ModuleDefinition.KEY_MODULE in self._db_values)


class SubTypeCounter:

    def __init__(self):
        self.timestamp = None
        self.subtype = None
        self.stubs = 0
        self.filled_stubs = 0
        self.empty_stubs = 0
        self.nonstubs = 0
        self.filled_nonstubs = 0
        self.empty_nonstubs = 0

    def add_component(self, timestamp, thing):
        if self.timestamp is None:
            self.timestamp = timestamp
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

    def __iter__(self):
        yield self.timestamp
        yield self.subtype
        yield self.stubs
        yield self.filled_stubs
        yield self.empty_stubs
        yield self.nonstubs
        yield self.filled_nonstubs
        yield self.empty_nonstubs


class StubsMetric(DataMetric):

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
        result = [ModuleDefinition(dbv) for dbv in result]
        return result

    def get_components(self):
        sparql_query = '''SELECT ?type ?subtype ?stub ?sequence ?component
                                 ?sequenceAnnotation
          WHERE {
              ?type <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ComponentDefinition> .
              ?type <http://sbols.org/v2#type> ?subtype .
              OPTIONAL { ?type <http://sd2e.org#stub_object> ?stub }
              OPTIONAL { ?type <http://sbols.org/v2#sequence> ?sequence }
              OPTIONAL { ?type <http://sbols.org/v2#component> ?component }
              OPTIONAL { ?type <http://sbols.org/v2#sequenceAnnotation> ?sequenceAnnotation }
              FILTER (! strstarts(str(?subtype), "http://identifiers.org/so/SO:"))
          }
        '''
        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result,
                                                 ['type', 'subtype', 'stub',
                                                  'sequence', 'component',
                                                  'sequenceAnnotation'])
        result = [ComponentDefinition(dbv) for dbv in result]
        return result

    def fetch(self):
        timestamp = int(time.time())
        rows = collections.defaultdict(SubTypeCounter)
        modules = self.get_modules()
        for m in modules:
            rows[m.subtype].add_component(timestamp, m)
        components = self.get_components()
        for c in components:
            rows[c.subtype].add_component(timestamp, c)
        return sorted(rows.values(), key=lambda x: x.subtype)
