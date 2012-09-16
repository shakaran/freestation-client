#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

import sys

import gi
try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst, GstVideo
except ValueError:
    print 'Could not find required Gstreamer 1.0 library.'
    sys.exit(1)
    
# Setup GStreamer 
Gst.init(None)
Gst.init_check(None)
print Gst.version_string(), Gst.version()

if Gst.ElementFactory.find('playbin'):
    player = Gst.ElementFactory.make('playbin', 'MultimediaPlayer')
    
    for x in dir(player):
        print x
    
    if player == None:
        print 'Error: could not create the player'
        sys.exit(1)
    else:
        # http://developer.gnome.org/gstreamer/unstable/GstSystemClock.html 
        # http://developer.gnome.org/gstreamer/unstable/GstClock.html 

        player_clock = player.get_clock() # Gets the current clock used by pipeline.

        system_clock = player_clock.obtain() # SystemClock 
        print system_clock.clock # (RuntimeError: unable to get the value)
        #print system_clock.clock-type # (RuntimeError: unable to get the value)
        #print system_clock.realtime # AttributeError: 'SystemClock' object has no attribute 'realtime'
        #print system_clock.monotonic # AttributeError: 'SystemClock' object has no attribute 'monotonic
        
else:
    print 'Error: could not find the playbin plugin for gstreamer'
    sys.exit(1)
