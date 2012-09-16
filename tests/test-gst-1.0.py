#!/usr/bin/python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

# gst-inspect-1.0 playbin
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

print Gst.version_string()

pipeline=Gst.ElementFactory.make('playbin', None)
pipeline.set_property('uri','file:///freestation/ogv/orbit.ogv')
pipeline.set_state(Gst.State.PLAYING)

bus=pipeline.get_bus()

# still a little problem with the annotation for this
# msg=bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE,Gst.MessageType.EOS | Gst.MessageType.ERROR)
# ValueError: -1 not in range 0 to 18446744073709551615
GST_CLOCK_TIME_NONE=18446744073709551615

# wait for preroll or error
msg=bus.timed_pop_filtered(GST_CLOCK_TIME_NONE, Gst.MessageType.ASYNC_DONE | Gst.MessageType.ERROR)

if msg.type == Gst.MessageType.ASYNC_DONE:
  ret, dur = pipeline.query_duration(Gst.Format.TIME)
  print "Duration: %u seconds" % (dur / Gst.SECOND)

  # wait for EOS or error
  msg=bus.timed_pop_filtered(GST_CLOCK_TIME_NONE, Gst.MessageType.EOS | Gst.MessageType.ERROR)

if msg.type == Gst.MessageType.ERROR:
  gerror, dbg_msg = msg.parse_error()
  print "Error         : ", gerror.message
  print "Debug details : ", dbg_msg

pipeline.set_state(Gst.State.NULL)