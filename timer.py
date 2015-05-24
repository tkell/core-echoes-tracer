#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import json
from time import sleep
from subprocess import check_output
from subprocess import CalledProcessError
import requests

def pop_from_redis():
    url = 'https://core-echoes.herokuapp.com/delete_route'
    res = requests.delete(url)
    return res.json()

def get_from_redis():
    url = 'https://core-echoes.herokuapp.com/route'
    res = requests.get(url)
    return res.json()

def get_count_from_redis():
    url = 'https://core-echoes.herokuapp.com/count'
    res = requests.get(url)
    return res.json()['count']

# IP times, in seconds
def get_time_for_ip(ip):
    numbers = ip.split('.')[0:3]
    time = 0
    for number in numbers:
        for digit in number:
            time = time + int(digit)
    return time

def get_time_for_trace(trace):
    time = 0
    for item in trace:
        time = time + get_time_for_ip(item['ip'])
    return time / 4
    
if __name__ == '__main__':
    next_trace = get_from_redis()
    next_trace_time = get_time_for_trace(next_trace)
    start_time = time.time()
    print "Starting. Time is %d" % start_time
    while True:
        # if we should move on to the next trace, remove the old trace
        now = time.time()
        if start_time + next_trace_time <= now:
            print "timed out:  removing an old trace and getting the time for the next trace"
            next_trace = pop_from_redis()
            next_trace_time = get_time_for_trace(next_trace)
            print "next trace time is %d" % next_trace_time
            start_time = now

