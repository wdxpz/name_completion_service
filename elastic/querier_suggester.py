import re
import os
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers


from elastic.scripts_suggester import Suggester_Index_Name, Body_To_Create_Name_Suggester_Index, build_query_Name_Suggester_Data
from utils.logger import getLogger 
logger = getLogger(__name__)
logger.propagate = False


class QuerierSuggester:

    def __init__(self, hosts=None) -> None:
        super().__init__()

        self.indexName = Suggester_Index_Name
        self.docMapping = Body_To_Create_Name_Suggester_Index

        if hosts is None:
            self.es = Elasticsearch([{'host': 'host.docker.internal'}])#for ubuntu, the host value should be set to 172.17.0.1, for macos, set as host.docker.internal
        else:
            self.es = Elasticsearch(hosts)

    def create_index(self):
        if self.es.indices.exists(index=self.indexName):
            logger.info('index %s already exists', self.indexName)
            self.delete_index()

        logger.info('creating index %s', self.indexName)
        self.es.indices.create(index=self.indexName, body=self.docMapping)

    def delete_index(self):
        self.es.indices.delete(index=self.indexName, ignore=[400, 404])

    def index_data_from_file(self, cachefile):
        if cachefile is None or not os.path.exists(cachefile):
            msg = 'error to find name data file'
            logger.info(msg)
            raise Exception(msg)

        try:
            all_data = []
            with open(cachefile, 'r') as file:
                content = file.read()
                all_data = json.loads(content)
            self.index_data(all_data)
        except Exception as e:
            msg = 'error to parse name data file: ' + str(e)
            logger.info(msg)
            raise Exception(msg)
    
    def index_data(self, all_data):
        action = ({
            "_index": self.indexName,
            "suggester": {
                "input": self.split_name_for_suggester(data['en_name'], data['ch_name']),
                # "weight": 1000 - len(data['name']])
            },
            "display_name": data['ch_name']+'|'+data['en_name'],
            "employee_id": data['id'],
            } for data in all_data if set(['ch_name', 'en_name', 'id'])==set(data.keys()))
        helpers.bulk(self.es, action)

    def query(self, keyword, groupsize=5):
        results = {
            "total": 0,
            "results": []
        }

        try:
            query_body = build_query_Name_Suggester_Data(keyword, groupsize)
        except ValueError:
            return results
        finally:
            pass

        query_results = self.es.search(index=self.indexName, body=query_body)
        bucket = query_results['suggest']['name_suggest'][0]['options']
        results['total'] += len(bucket)
        for item in bucket:
            results['results'].append({
                'uuid': item['_source']['employee_id'],
                'name': item['_source']['display_name']
            })

        return results

    @staticmethod
    def split_name_for_suggester(en_name, ch_name):

        #en_name is mandatory
        if en_name is None or len(en_name)==0:
            return []
        
        employee_name = en_name
        if ch_name is not None and len(ch_name)>0:
            ch_name_list = [ch_name[i:] for i in range(len(ch_name))]
            employee_name = ' '.join(ch_name_list) + ' ' + employee_name

        employee_name = employee_name.lower()

        results = [employee_name]

        # and remove '(' and ')'
        employee_name = re.sub('\(|\)', ' ', employee_name)

        # split by ' '
        p = re.compile(' ')
        splits_by_blank = p.split(employee_name)

        # results = []
        if len(splits_by_blank)==1:
            return results

        for i in range(1, len(splits_by_blank)):
            results.append(' '.join(splits_by_blank[i:]))

        return results
