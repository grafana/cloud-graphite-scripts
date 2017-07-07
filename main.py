import requests
from datetime import datetime, timedelta

GRAFANA_URL = 'https://<your-subdomain>.hosted-metrics.grafana.net/metrics'
GRAFANA_APIKEY = '<your api key from grafana.net -- should be editor role>'


def write_metrics(metrics, url, apikey):
    headers = {
        "Authorization": "Bearer %s" % apikey
    }
    grafana_data = []
    for m in metrics:
        grafana_data.append(
            {
                'name': m[0],
                'metric': m[0],
                'value': float(m[2]),
                'interval': int(m[1]),
                'unit': '',
                'time': int(m[3].timestamp()),
                'mtype': 'count',
                'tags': [],
            }
        )
    result = requests.post(url, json=grafana_data, headers=headers)
    if result.status_code != 200:
        raise Exception(result.text)
    print('%s: %s' % (result.status_code, result.text))


now = datetime.now()
metrics = [
    ('my.test.metric', 10, 0.23, now - timedelta(seconds=30)),
    ('my.test.metric', 10, 1.23, now - timedelta(seconds=20)),
    ('my.test.metric', 10, 2.23, now - timedelta(seconds=10)),
    ('my.test.metric', 10, 3.23, now),
]

write_metrics(metrics, GRAFANA_URL, GRAFANA_APIKEY)
