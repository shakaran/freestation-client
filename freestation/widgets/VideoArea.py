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

from freestation.logger import Logger
LOG = Logger('VideoArea').get()

import sys
import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    print ('Could not find required Gtk 3.0 library.')
    sys.exit(1)
    
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print ('Could not find required Gstreamer 1.0 library.')
    sys.exit(1)
    
from gi.repository import GdkX11, Gtk, Gdk #@UnresolvedImport @UnusedImport
from gi.repository import Gst, GstVideo  #@UnresolvedImport @UnusedImport
from gi.repository import GObject #@UnresolvedImport @UnusedImport

GObject.threads_init()

class VideoArea(Gtk.DrawingArea): 
    __gtype_name__ = 'VideoArea'
        
    def __init__(self, video):
        Gtk.DrawingArea.__init__(self)
        self.show()
        
        # https://bugzilla.gnome.org/show_bug.cgi?id=663360 Don't use get_window()
        
        
        self.video = video
        #self.xid = xid
        
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON1_MOTION_MASK )
        
        self.set_size_request(480, 320)
        self.create_player()
        
    def create_player(self):
        # Setup GStreamer 
        Gst.init(None)
        
        self.player = Gst.ElementFactory.make('playbin', 'MultimediaPlayer')
        
    def load_player(self):
        
        self.bus = self.player.get_bus() 
        self.bus.add_signal_watch() 
        self.bus.enable_sync_message_emission()
        self.bus.connect('message::eos', self.on_message_eos)
        
        assert self.player.set_state(Gst.State.NULL) == Gst.StateChangeReturn.SUCCESS

        assert self.player.set_state(Gst.State.READY) == Gst.StateChangeReturn.SUCCESS
        
        #self.player.set_property('uri', 'file://' + self.video) 
        self.player.set_property('uri', 'http://docs.gstreamer.com/media/sintel_trailer-480p.webm') 
        
        self.player.set_state(Gst.State.PLAYING)
        
    def play(self):
        self.player.set_state(Gst.State.PLAYING)
        
    def on_message_eos(self, bus, message):
        """ 
            EOS: End of Stream
            When the video finished plays again seeking to start
        """
        self.player.seek_simple(
            Gst.Format.TIME,        
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )
        
