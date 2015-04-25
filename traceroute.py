#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from time import sleep
from subprocess import check_output
from subprocess import CalledProcessError
import requests

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


print get_trace("56.33.199.10")

## loop sketches:
# ip_generator = get_all_ips()
# next_ip = ip_generator.next()
# old_trace = []
# new_trace = []
# while true:
#     if server.is_full: ## or something
#         continue
#     else:
#         old_trace = trace(next_ip)
#         final_trace = interpolate(old_trace, new_trace)
#         # put final_trace somewhere:  server.put(final_trace)
#         old_trace = new_trace
#         next_ip = ip_genertor.next()
# 
