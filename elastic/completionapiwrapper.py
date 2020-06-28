#from elastic.querier_nagram import QuerierNgram
from elastic.querier_suggester import QuerierSuggester

#complete_engine = QuerierNgram()
complete_engine = QuerierSuggester()


def query_completion(qury_words):
    if complete_engine is None:
        raise Exception("failed to connect Elastic engine!")

    resutls = complete_engine.query(qury_words)

    completion_list = []
    for item in resutls['results']:
        completion_list.append(item['uuid'] + ' ' + item['name'])

    return completion_list

def create_name_index(all_data):
    if complete_engine is None:
        raise Exception("failed to connect Elastic engine!")
    complete_engine.create_index()
    complete_engine.index_data(all_data)
    