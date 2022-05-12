#!/bin/bash

key="<user_id>:<api-key>"
addr="https://<your-instance>.hosted-metrics.grafana.net"

curl -X POST -H "Authorization: Bearer $key" -H "Content-Type: application/json" "$addr/metrics" -d '[{
    "name": "test.metric",
    "interval": 10,
    "value": 12.345,
    "time": 1534685580
},
{
    "name": "test.metric",
    "interval": 10,
    "value": 12.345,
    "time": 1534685590
    }
]'
