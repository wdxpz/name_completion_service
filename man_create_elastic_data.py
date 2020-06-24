import os
import time

from elastic.querier_suggester import QuerierSuggester

querier = QuerierSuggester()
querier.create_index()
querier.index_data("employ.csv")



es = QuerierSuggester()
querys = ['sens', 'he', 'th', 'time t', 'on o', 'coffe', 'sensexiting', 'weather', 'wea', 'bo', 'cak', 'lak',
                  'light', 'case', 'ice', 'choco', 'comput', 'class', 'object', 'worker']
start = time.time()
for word in querys:
    results = es.query(word, 5)

duration = time.time() - start
avarage_time = duration*1000.0 / len(querys)

print('average query time by suggester querier: {} ms'.format(avarage_time))



