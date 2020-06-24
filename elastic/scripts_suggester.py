Suggester_Max_Length = 50
Suggester_Index_Name = "name_suggester_index"


Body_To_Create_Name_Suggester_Index = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "index.store.preload": ["nvd", "dvd", "tim", "doc", "dim"],
    },
    "mappings": {
        # Suggester_Type_Name: {
            "properties": {
                "suggester": {
                    "type": "completion",
                    "analyzer": "simple",
                    "search_analyzer": "simple",
                },
                "display_name": {
                    "type": "keyword",
                    "index": "false",
                    "doc_values": "false"
                },
                "employee_id": {
                    "type": "keyword",
                    "index": "false",
                    "doc_values": "false"
                },
            }
 #       }
    }
}

Body_To_Query_Name_Suggester_Data = {
    "suggest": {
        "name_suggest": {
            "prefix": "wu",
            "completion": {
                "field": "suggester",
                "size": 5,
            }
        },
    }
}


def build_query_Name_Suggester_Data(keyword, groupsize=5):
    if keyword is None:
        raise ValueError("query keyword is None!")

    if groupsize < 1:
        groupsize = 3

    Body_To_Query_Name_Suggester_Data["suggest"]["name_suggest"]["prefix"] = keyword.lower()
    Body_To_Query_Name_Suggester_Data["suggest"]["name_suggest"]["completion"]["size"] = groupsize

    return Body_To_Query_Name_Suggester_Data
