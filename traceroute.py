#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
import json
from time import sleep
from subprocess import check_output
from subprocess import CalledProcessError
import requests

# How do I deal with very short traceroutes?  There's a long-term race condition here...
def get_all_ips(starting_ip):
    ip_array = [int(ip) for ip in starting_ip.split('.')]

    for x1 in range(ip_array[0], 256):
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
        for x2 in range(ip_array[1], 256):
            if x1 == 100 and x2 == 64:
                continue
            if x1 == 169 and x2 == 254:
                continue
            if x1 == 172 and x2 == 16:
                continue
            if x1 == 198 and x2 == 18:
                continue
            for x3 in range(ip_array[2], 256):
                if x1 == 198 and x2 == 51 and x3 == 100:
                    continue
                if x1 == 203 and x2 == 0 and x3 == 113:
                    continue
                for x4 in range(ip_array[3], 256):
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

# Just cuts the first two ips, as they're pure amazon
def interpolate(new_trace):
    if len(new_trace) > 2:
        new_trace = new_trace[2:]
    return new_trace

# sends things to the server
def send_to_redis(trace, target):
    data = {"target": target, "trace": trace}
    url = 'https://core-echoes.herokuapp.com/add_route'
    res = requests.post(url, data=json.dumps(data))
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
    starting_ip = sys.argv[1]
    old_trace = []
    new_trace = []
    ip_generator = get_all_ips(starting_ip)

    print "getting %d initial traces" % filler_count
    for x in range(filler_count): 
        next_ip = ip_generator.next()
        print next_ip
        new_trace = get_trace(next_ip)
        final_trace = interpolate(new_trace)
        if len(final_trace) == 0:
            continue
        send_to_redis(final_trace, next_ip)
        old_trace = new_trace
    
    while True:
        # Fill the server
        try:
            count = get_count_from_redis()
        except requests.exceptions.ConnectionError:
            time.sleep(4)
        if count > 100:
            print "server has %d things, sleeping for 2 seconds" % count
            time.sleep(2)
        else:
            print "server has fewer than 100 things, adding a trace"
            next_ip = ip_generator.next()
            new_trace = get_trace(next_ip)
            final_trace = interpolate(new_trace)
            if len(final_trace) == 0:
                continue
            send_to_redis(final_trace, next_ip)
            old_trace = new_trace
 
