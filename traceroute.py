#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import json
from time import sleep
from subprocess import check_output
from subprocess import CalledProcessError
import requests

# How do I deal with very short traceroutes?  There's a long-term race condition here...
def get_all_ips():
    for x1 in range(1, 255):
        if x1 == 10:
            continue
        if x1 == 127:
            continue
        if x1 == 192:
            continue
        if x1 == 198:
            continue
        if x1 == 224:
            continue
        if x1 == 240:
            continue
        for x2 in range(255):
            if x1 == 100 and x2 == 64:
                continue
            if x1 == 169 and x2 == 254:
                continue
            if x1 == 172 and x2 == 16:
                continue
            if x1 == 198 and x2 == 18:
                continue
            for x3 in range(255):
                if x1 == 198 and x2 == 51 and x3 == 100:
                    continue
                if x1 == 203 and x2 == 0 and x3 == 113:
                    continue
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
    if final_trace[-1]['ip'] not in new_ips:
        return new_trace
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
    
filler_count = 10
if __name__ == '__main__':
    print "Setting up arrays and generators"    
    old_trace = []
    new_trace = []
    ip_generator = get_all_ips()

    print "getting %d initial traces" % filler_count
    for x in range(filler_count): 
        next_ip = ip_generator.next()
        new_trace = get_trace(next_ip)
        final_trace = interpolate(old_trace, new_trace)
        if len(final_trace) == 0:
            continue
        send_to_redis(final_trace)
        old_trace = new_trace
    
    while True:
        # Fill the server
        count = get_count_from_redis()
        if count > 100:
            print "server has %d things, sleeping for 2 seconds" % count
            time.sleep(2)
        else:
            print "server has fewer than 100 things, adding a trace"
            next_ip = ip_generator.next()
            new_trace = get_trace(next_ip)
            final_trace = interpolate(old_trace, new_trace)
            if len(final_trace) == 0:
                continue
            send_to_redis(final_trace)
            old_trace = new_trace
 
