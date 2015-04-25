#!/usr/bin/env python
# -*- coding: utf-8 -*-

# I need a function to ask for a trace to an IP, 
# and then interpolate it with the previous trace.

# and I need to wrap this all in something really robust


def get_all_ips():
    for x1 in range(255):
        for x2 in range(255):
            for x3 in range(255):
                for x4 in range(255):
                    yield "%s.%s.%s.%s" % (x1, x2, x3, x4)

