from constants import Doc_Fields, Indexed_Doc_Categories

Suggester_Max_Length = 50
Suggester_Index_Name = "thingin_suggester_index"
Suggester_Type_Name = "thingin_suggester_type"

Body_To_Create_Thingin_Suggester_Index = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "index.store.preload": ["nvd", "dvd", "tim", "doc", "dim"],
    },
    "mappings": {
        # Suggester_Type_Name: {
            "properties": {
                Doc_Fields['ont_name_suggester_field']: {
                    "type": "completion",
                    "analyzer": "simple",
                    "search_analyzer": "simple",
                    "contexts": [{
                        "name": "type",
                        "type": "category",
                        "path": Doc_Fields['ont_type']
                    }]
                },
                Doc_Fields['ont_type']: {
                    "type": "keyword",
                    "index": "true",
                    "eager_global_ordinals": "true"
                },
                Doc_Fields['ont_name']: {
                    "type": "keyword",
                    "index": "false",
                    "doc_values": "false"
                },
                Doc_Fields['ont_iri']: {
                    "type": "text",
                    "index": "false",
                    "doc_values": "false"
                },
                Doc_Fields['ont_description']: {
                    "type": "text",
                    "index": "false",
                    "doc_values": "false"
                },
                Doc_Fields['ont_comment']: {
                    "type": "text",
                    "index": "false",
                    "doc_values": "false"
                }
            }
 #       }
    }
}

Body_To_Query_Thingin_Suggester_Data = {
    "suggest": {
        Indexed_Doc_Categories[0]: {
            "prefix": "sens",
            "completion": {
                "field": "suggester",
                "size": 5,
                "contexts": {
                    "type": Indexed_Doc_Categories[0]
                }
            }
        },
        Indexed_Doc_Categories[1]: {
            "prefix": "sens",
            "completion": {
                "field": "suggester",
                "size": 5,
                "contexts": {
                    "type": Indexed_Doc_Categories[1]
                }
            }
        },
        Indexed_Doc_Categories[2]: {
            "prefix": "sens",
            "completion": {
                "field": "suggester",
                "size": 5,
                "contexts": {
                    "type": Indexed_Doc_Categories[2]
                }
            }
        }
    }
}


def build_query_Thingin_Suggester_Data(keyword, groupsize=5):
    if keyword is None:
        raise ValueError("query keyword is None!")

    if groupsize < 1:
        groupsize = 3

    for i in range(len(Indexed_Doc_Categories)):
        Body_To_Query_Thingin_Suggester_Data["suggest"][Indexed_Doc_Categories[i]]["prefix"] = keyword.lower()
        Body_To_Query_Thingin_Suggester_Data["suggest"][Indexed_Doc_Categories[i]]["completion"]["size"] = groupsize


    return Body_To_Query_Thingin_Suggester_Data
