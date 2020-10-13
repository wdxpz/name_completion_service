# Elasticsearch DSL query for name autocompletion
## start the whole service
```
sudo sysctl -w vm.max_map_count=262144  #otherwise, it will report bootstrap checks failed when start elasticsearch node after reboot
cd project_dir
sudo docker-compose up
```
## some web apis
### cluster health
```
curl -X GET "localhost:9200/_cat/health?v&pretty"
```

### all indeices
```
curl "localhost:9200/_cat/indices?v"
```

### index data
```
curl -X PUT "localhost:9200/customer/_doc/2?pretty" -H 'Content-Type: application/json' -d'
{
  "name": "吴思 wu si"
}
'
{
  "_index" : "customer",
  "_type" : "_doc",
  "_id" : "2",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```


### query data
* use wildcard query to do in_word matching
```
curl -X GET "localhost:9200/customer/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "wildcard": { "name": "*xi*" } }
}
'

{
  "took" : 12,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "customer",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "name" : "吴晓笛 wu xiaodi"
        }
      }
    ]
  }
}
```
* `match` query can match `晓` with `吴晓`, or `xiao` with `xiaodi`, but not `xia` with `xiao`
```
curl -X GET "localhost:9200/customer/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match": { "name": "晓" } }
}
'

{
  "took" : 11,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.8538153,
    "hits" : [
      {
        "_index" : "customer",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.8538153,
        "_source" : {
          "name" : "吴晓笛 wu xiaodi"
        }
      }
    ]
  }
}
```
