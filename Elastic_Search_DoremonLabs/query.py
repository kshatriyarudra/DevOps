import json

with open("cfg.json") as json_data_file:
    data = json.load(json_data_file)

body={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        "response_code": 200
                    }
                },
                "filter":{
                    "range":{
                        "@timestamp":{
                            "gte":data['details']['start_date_time'],
                            "lte":data['details']['end_date_time']
                        }
                    }
                }
            }
        }
    }

body1={
        'query':{
            'bool':{
                'must':{
                    'match':{
                        "response_code": 500
                    }
                },
                "filter":{
                    "range":{
                        "response_time":{
                            "gte":400,
                            "lte":500
                        }
                    }
                }
            }
        }
    }

