#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

import sys

import gi
try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
except ValueError:
    print 'Could not find required Gstreamer 1.0 library.'
    sys.exit(1)
    
# Setup GStreamer 
Gst.init(None)
Gst.init_check(None)
print Gst.version_string(), Gst.version()

Gst.debug_set_active(True) # If activated, debugging messages are sent to the debugging handlers.

for x in dir(Gst.DebugCategory()):
    print x
    
Gst.debug_log_default(
                          category = Gst.DebugCategory(), 
                          level = Gst.DebugLevel.ERROR,
                          file = 'gst-error.log',
                          function = 'myfunction',
                          line = '100',
                          object = 'myobject',
                          message = 'this is a error', 
                          unused = 0,
                      )