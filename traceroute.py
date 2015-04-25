#!/usr/bin/env python
# -*- coding: utf-8 -*-

# I need a function to ask for a trace to an IP, 
# and then interpolate it with the previous trace.

# and I need to wrap this all in something really robust

import re
from subprocess import check_output

def get_all_ips():
    for x1 in range(255):
        for x2 in range(255):
            for x3 in range(255):
                for x4 in range(255):
                    yield "%s.%s.%s.%s" % (x1, x2, x3, x4)

def get_trace(ip):
    trace = []
    res = check_output(['traceroute', '65.34.111.200'])
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


trace = get_trace("test")
print trace
