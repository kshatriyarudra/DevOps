
import config as cfg

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
                            "gte":cfg.elastic_search['start_date_time'],
                            "lte":cfg.elastic_search['end_date_time']
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
                            "gte":100,
                            "lte":500
                        }
                    }
                },
                "filter":{
                    "range":{
                        "@timestamp":{
                            "gte":cfg.elastic_search['start_date_time'],
                            "lte":cfg.elastic_search['end_date_time']
                        }
                    }
                }
            }
        }
    }

