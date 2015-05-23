#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import json
from time import sleep
from subprocess import check_output
from subprocess import CalledProcessError
import requests

# This needs some restrictions to avoid, say, 0.x.x.x, 127, etc
def get_all_ips():
    for x1 in range(255):
        for x2 in range(255):
            for x3 in range(255):
                for x4 in range(255):
                    yield "%s.%s.%s.%s" % (x1, x2, x3, x4)

def get_trace(ip):
    trace = []
    try:
        res = check_output(['traceroute', ip])
    except CalledProcessError:
        res = ''

    lines = res.split('\n')
    for line in lines:
        res = re.search(r'\d  (.+)', line)
        if not res:
            continue
        line_text = res.group(1)
        res = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', line_text)
        if not res:
            continue
        ip = res.group(1)
        trace.append({'ip': ip, 'line_text': line_text})

    return trace

# Returns a path from old_trace to new_trace!
def interpolate(old_trace, new_trace):
    if old_trace == []:
        return new_trace

    final_trace = []
    new_ips = [t['ip'] for t in new_trace]
    old_trace.reverse()

    for trace in old_trace:
        if trace['ip'] not in new_ips:
            final_trace.append(trace)
        else:
            final_trace.append(trace)
            break
    new_index = new_ips.index(final_trace[-1]['ip'])
    for trace in new_trace[new_index + 1:]:
        final_trace.append(trace)

    return final_trace[1:]

# sends things to the server
def send_to_redis(trace):
    url = 'https://core-echoes.herokuapp.com/add_route'
    res = requests.post(url, data=json.dumps(trace))
    return res

def pop_from_redis():
    url = 'https://core-echoes.herokuapp.com/delete_route'
    res = requests.delete(url)
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
#     old_trace = []
#     new_trace = []
#     ip_generator = get_all_ips()
# 
#     next_ip = ip_generator.next()
#     new_trace  = trace(next_ip)
#     final_trace = interpolate(old_trace, new_trace)
#     send_to_redis(final_trace)
#     old_trace = new_trace
# 
#     next_trace_time = get_time_for_trace(final_trace)
#     start_time = time.time()
# 
#     while true:
#         # if we should move on to the next trace, remove the old trace
#         now = time.time()
#         if start_time + next_trace_time > now:
#             next_trace = pop_from_redis() ## this needs to return the NEXT TRACE, so we can get the time for it.
#             next_trace_time = get_time_for_trace(next_trace)
#             start_time = now
#         
#         # main functionality
#         count = get_server_count()
#         if count > 100:
#             time.sleep(2)
#         else:
#             next_ip = ip_generator.next()
#             new_trace  = trace(next_ip)
#             final_trace = interpolate(old_trace, new_trace)
#             send_to_redis(final_trace)
#             old_trace = new_trace
# 
