#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# This file is part of FreeStation.
#
# FreeStation is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# FreeStation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fail2Ban; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Author: Ángel Guzmán Maeso
# 
# $Revision$

__author__    = 'Ángel Guzmán Maeso'
__version__   = '$Revision$'
__date__      = '$Date$'
__copyright__ = 'Copyright (c) 2012 Ángel Guzmán Maeso'
__license__   = 'GPL'

import gtk
import pygtk
pygtk.require('2.0')
#import gobject
import pygst
pygst.require('0.10')
import gst
import os, sys

print gst.version_string()
print gst.version()
print gst.__file__

class Video:

    def __init__(self):

        def on_message(bus, message): 
            if message.type == gst.MESSAGE_EOS: 
                # End of Stream 
                player.set_state(gst.STATE_NULL) 
            elif message.type == gst.MESSAGE_ERROR: 
                player.set_state(gst.STATE_NULL) 
                (err, debug) = message.parse_error() 
                print "Error: %s" % err, debug

        def on_sync_message(bus, message):
            if message.structure is None: 
                return False 
            if message.structure.get_name() == "prepare-xwindow-id":
                if sys.platform == "win32":
                    win_id = videowidget.window.handle
                else:
                    win_id = videowidget.window.xid
                assert win_id
                
                gtk.gdk.threads_enter()
                gtk.gdk.display_get_default().sync()
                imagesink = message.src 
                imagesink.set_property("force-aspect-ratio", True)
                imagesink.set_xwindow_id(win_id) 
                gtk.gdk.threads_leave()

        win = gtk.Window()
        win.set_resizable(False)
        win.set_has_frame(False)
        win.set_position(gtk.WIN_POS_CENTER)

        fixed = gtk.Fixed()
        win.add(fixed)
        fixed.show()

        videowidget = gtk.DrawingArea()
        fixed.put(videowidget, 0, 0)
        videowidget.set_size_request(640, 480)
        videowidget.show()

        # Setup GStreamer 
        player = gst.element_factory_make("playbin", "MultimediaPlayer")
        bus = player.get_bus() 
        bus.add_signal_watch() 
        bus.enable_sync_message_emission() 
        #used to get messages that GStreamer emits 
        bus.connect("message", on_message) 
        #used for connecting video to your application 
        bus.connect("sync-message::element", on_sync_message)
        player.set_property("uri", "file://" + "freestation/ogv/orbit.ogv") 
        player.set_state(gst.STATE_PLAYING)

        win.show()

def main():
    gtk.gdk.threads_init()
    gtk.main()
    return 0

if __name__ == "__main__":
    Video()
    main()