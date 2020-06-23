#from elastic.querier_nagram import QuerierNgram
from elastic.querier_suggester import QuerierSuggester

#complete_engine = QuerierNgram()
complete_engine = QuerierSuggester()


def query_completion(qury_words):
    resutls = complete_engine.query(qury_words)

    completion_list = []
    for key in resutls['results'].keys():
         ontoloty_list = resutls['results'][key]
         for item in ontoloty_list:
             completion_list.append(key+':' + item['name'] + ' ' + item['iri'] + ' ' + item['description'] + ' ' + item['comment'])

    return completion_list