import re

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import pickle
import logging

from constants import Indexed_Doc_Categories
from elastic.scripts_suggester import *

logger = logging.getLogger(__name__)


class QuerierSuggester:

    def __init__(self, hosts=None) -> None:
        super().__init__()

        self.indexName = Suggester_Index_Name
        self.typeName = Suggester_Type_Name
        self.docMapping = Body_To_Create_Thingin_Suggester_Index

        if hosts is None:
            self.es = Elasticsearch([{'host': 'host.docker.internal'}])#for ubuntu, the host value should be set to 172.17.0.1, for macos, set as host.docker.internal
        else:
            self.es = Elasticsearch(hosts)

    def create_index(self):
        if self.es.indices.exists(index=self.indexName):
            logger.info('index %s already exists', self.indexName)
            self.delete_index()

        logger.info('creating index %s and type %s', self.indexName, self.typeName)
        self.es.indices.create(index=self.indexName, body=self.docMapping)

    def delete_index(self):
        self.es.indices.delete(index=self.indexName, ignore=[400, 404])


    def index_data(self, cachefile):

        if cachefile is None or not os.path.exists(cachefile):
            logger.info('error to find thingin data cache file')

        with open(cachefile, 'rb') as file:
            all_data = pickle.load(file)

        action = ({
            "_index": self.indexName,
            # "_type": self.typeName,
            Doc_Fields['ont_name_suggester_field']: {
                "input": self.split_thingin_class_name_for_suggester(data[Doc_Fields['ont_name']]),
                "weight": 1000 - len(data[Doc_Fields['ont_name']])
            },
            Doc_Fields['ont_name']: data[Doc_Fields['ont_name']],
            Doc_Fields['ont_type']: data[Doc_Fields['ont_type']],
            Doc_Fields['ont_iri']: data[Doc_Fields['ont_iri']],
            Doc_Fields['ont_description']: data[Doc_Fields['ont_description']],
            Doc_Fields['ont_comment']: data[Doc_Fields['ont_comment']]
            } for data in all_data)

        helpers.bulk(self.es, action)

    def query(self, keyword, groupsize=5):
        results = {
            "total": 0,
            "results": {
                Indexed_Doc_Categories[0]: [],
                Indexed_Doc_Categories[1]: [],
                Indexed_Doc_Categories[2]: [],
            }
        }

        try:
            query_body = build_query_Thingin_Suggester_Data(keyword, groupsize)
        except ValueError:
            return results
        finally:
            pass

        query_results = self.es.search(index=self.indexName, body=query_body)

        for i in range(len(Indexed_Doc_Categories)):
            bucket = query_results['suggest'][Indexed_Doc_Categories[i]][0]['options']
            results['total'] += len(bucket)
            for item in bucket:
                item['_source'].pop(Doc_Fields['ont_type'])
                item['_source'].pop('suggester')
                if item['_source'][Doc_Fields['ont_description']] is None:
                    item['_source'][Doc_Fields['ont_description']] = ''
                if item['_source'][Doc_Fields['ont_comment']] is None:
                    item['_source'][Doc_Fields['ont_comment']] = ''

                results['results'][Indexed_Doc_Categories[i]].append(item['_source'])

        return results

    @staticmethod
    def split_thingin_class_name_for_suggester(class_name):

        def split_by_capital(phase):
            splits = []
            if phase.isupper():
                splits = [phase]
            else:
                # split by capital letter
                splits = re.findall('[A-Z][^A-Z]*', phase)
                if len(splits)>0:
                    if phase.find(splits[0])>0:
                        splits = [phase[0:phase.find(splits[0])]] + splits
                else:
                    splits = [phase]
            return splits

        if class_name is None or len(class_name)==0:
            return []

        results = [class_name]

        # and remove '(' and ')'
        class_name = re.sub('\(|\)', '', class_name)

        # split by '-|_'
        p = re.compile('-|_')
        splits_by_bar = p.split(class_name)

        splits_by_up_letter = []
        for item in splits_by_bar:
            splits_by_up_letter = splits_by_up_letter + split_by_capital(item)
        # remove ""
        splits_by_up_letter = [item for item in splits_by_up_letter if len(item)>0]

        # results = []
        for i in range(len(splits_by_up_letter)):
            results.append(' '.join(splits_by_up_letter[i:]).lower())


        return results
