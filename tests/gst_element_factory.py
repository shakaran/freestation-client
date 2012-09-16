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

print 'ELEMENT_FACTORY_TYPE_AUDIOVIDEO_SINKS:', Gst.ELEMENT_FACTORY_TYPE_AUDIOVIDEO_SINKS
print Gst.ElementFactory.list_get_elements(Gst.ELEMENT_FACTORY_TYPE_AUDIOVIDEO_SINKS, 10000)

print 'ELEMENT_FACTORY_TYPE_ANY:', Gst.ELEMENT_FACTORY_TYPE_ANY
# TypeError: Expected a Gst.Rank, but got int
print Gst.ElementFactory.list_get_elements(Gst.ELEMENT_FACTORY_TYPE_ANY, 10000)

"""
    <constant name="ELEMENT_FACTORY_TYPE_ANY"
              value="-1"
              c:type="GST_ELEMENT_FACTORY_TYPE_ANY">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_AUDIOVIDEO_SINKS"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_AUDIOVIDEO_SINKS">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_AUDIO_ENCODER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_AUDIO_ENCODER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_DECODABLE"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_DECODABLE">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_DECODER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_DECODER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_DEMUXER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_DEMUXER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_DEPAYLOADER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_DEPAYLOADER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_ENCODER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_ENCODER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_FORMATTER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_FORMATTER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MAX_ELEMENTS"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MAX_ELEMENTS">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_ANY"
              value="-281474976710656"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_ANY">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_AUDIO"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_AUDIO">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_IMAGE"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_IMAGE">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_METADATA"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_METADATA">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_SUBTITLE"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_SUBTITLE">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MEDIA_VIDEO"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MEDIA_VIDEO">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_MUXER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_MUXER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_PARSER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_PARSER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_PAYLOADER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_PAYLOADER">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_SINK"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_SINK">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_SRC"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_SRC">
      <type name="gint" c:type="gint"/>
    </constant>
    <constant name="ELEMENT_FACTORY_TYPE_VIDEO_ENCODER"
              value="0"
              c:type="GST_ELEMENT_FACTORY_TYPE_VIDEO_ENCODER">
      <type name="gint" c:type="gint"/>
    </constant>
"""