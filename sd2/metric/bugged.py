
import collections
import logging
import time

from .api import DataMetric


class BuggedLinksMetric(DataMetric):

    def __init__(self, url):
        super().__init__(url)

    def get_module_defs(self):
        sparql_query = '''SELECT ?funcDef
          WHERE {
              ?thing <http://sbols.org/v2#functionalComponent> ?functionalComponent .
              ?functionalComponent <http://sbols.org/v2#definition> ?funcDef .
              ?funcDef <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ModuleDefinition> .
          }
        '''

        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['funcDef'])
        return result

    def get_component_defs(self):
        sparql_query = '''SELECT ?modDef
          WHERE {
              ?thing <http://sbols.org/v2#module> ?module .
              ?module <http://sbols.org/v2#definition> ?modDef .
              ?modDef <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://sbols.org/v2#ComponentDefinition> .
          }
        '''

        result = self._query.fetch_SPARQL(self._query._server,
                                          sparql_query)
        result = self._query.format_query_result(result, ['modDef'])
        return result

    def fetch(self):
        timestamp = int(time.time())
        result = []
        modules = self.get_module_defs()
        result.append([timestamp, 'Bugged Module Definitions', len(modules)])
        comp_defs = self.get_component_defs()
        result.append([timestamp, 'Bugged Component Definitions', len(comp_defs)])
        return result
