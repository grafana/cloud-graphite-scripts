#!/bin/bash

# See https://grafana.com/docs/grafana-cloud/data-configuration/metrics/metrics-graphite/http-api/#http-api 
key="<user_id>:<api-key>"
addr="graphite-<something>.grafana.net/graphite/metrics"

curl -X POST -H "Authorization: Bearer $key" -H "Content-Type: application/json" "$addr" -d '[{
    "name": "test.metric",
    "interval": 10,
    "value": 12.345,
    "time": 1676622710 # Note, this NEEDS to be updated with the current Unix time: https://www.unixtimestamp.com/
},
{
    "name": "test.metric",
    "interval": 10,
    "value": 67.891,
    "time": 1676622720 # Note, this NEEDS to be updated with the current Unix time + 10: https://www.unixtimestamp.com/
    }
]'
