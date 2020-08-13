#!/usr/bin/python

from __future__ import print_function

import requests
import json
import argparse
try:
  from Queue import Queue
except:
  from queue import Queue
from threading import Thread, Lock
import sys
import unicodedata

outLock = Lock()

def output(msg):
    with outLock:
        print(msg)
        sys.stdout.flush()

class Walker(Thread):
    def __init__(self, queue, url, user=None, password=None, seriesFrom=None, depth=None):
        Thread.__init__(self)
        self.queue = queue
        self.url = url
        self.user = user
        self.password = password
        self.seriesFrom = seriesFrom
        self.depth = depth


    def run(self):
        while True:
            branch = self.queue.get()
            try:
                branch[0].encode('ascii')
            except Exception as e:
                with outLock:
                    sys.stderr.write('found branch with invalid characters: ')
                    sys.stderr.write(unicodedata.normalize('NFKD', branch[0]).encode('utf-8','xmlcharrefreplace'))
                    sys.stderr.write('\n')
            else:
                if self.depth is not None and branch[1] == self.depth:
                    output(branch[0])
                else:
                    self.walk(branch[0], branch[1])
            self.queue.task_done()

    def walk(self, prefix, depth):
        payload = {
            "query": (prefix + ".*") if prefix else '*',
            "format": "treejson"
        }
        if self.seriesFrom:
            payload['from']=self.seriesFrom

        auth = None
        if self.user is not None:
            auth = (self.user, self.password)


        r = requests.get(
            self.url + '/metrics/find',
            params=payload,
            auth=auth,
        )

        if r.status_code != 200:
            sys.stderr.write(r.text+'\n')

            raise Exception(
                    'Error walking finding series: branch={branch} reason={reason}'
                .format(branch=unicodedata.normalize('NFKD', prefix).encode('ascii','replace'), reason=r.reason)
                )

        metrics = r.json()
        for metric in metrics:
            try:
                if metric['leaf']:
                    output(metric['id'])
                else:
                    self.queue.put((metric['id'], depth+1))
            except Exception as e:
                output(metric)
                raise e

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Graphite URL", required=True)
    parser.add_argument("--prefix", help="Metrics prefix", required=False, default='')
    parser.add_argument("--user", help="Basic Auth username", required=False)
    parser.add_argument("--password", help="Basic Auth password", required=False)
    parser.add_argument("--concurrency", help="concurrency", default=8, required=False, type=int)
    parser.add_argument("--from", dest='seriesFrom', help="only get series that have been active since this time", required=False)
    parser.add_argument("--depth", type=int, help="maximum depth to traverse. If set, the branches at the depth will be printed", required=False)
    args = parser.parse_args()
    url = args.url
    prefix = args.prefix
    user = args.user
    password = args.password
    concurrency = args.concurrency
    seriesFrom = args.seriesFrom
    depth = args.depth

    queue = Queue()

    for x in range(concurrency):
        worker = Walker(queue, url, user, password, seriesFrom, depth)
        worker.daemon = True
        worker.start()

    queue.put((prefix, 0))
    queue.join()
