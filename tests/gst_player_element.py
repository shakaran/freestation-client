#!/usr/bin/env python

import gi

gi.require_version('Gst', '1.0')

from gi.repository import GObject, Gtk, GdkX11, Gst, GstVideo

GObject.threads_init()
Gst.init(None)

def on_realize(window):
    win_id = window.get_window().get_xid()
    player.set_window_handle(win_id)
     
win = Gtk.Window()
fixed = Gtk.Fixed()
win.add(fixed)
fixed.show()

videowidget = Gtk.DrawingArea()
fixed.put(videowidget, 0, 0)
videowidget.set_size_request(640, 480)
videowidget.show()

player = Gst.ElementFactory.make('playbin', 'MultimediaPlayer')

bus = player.get_bus()

player.set_property('uri', 'file:///freestation/ogv/orbit.ogv') 

#win.connect('realize', on_realize)
win.realize()

win_id = win.get_window().get_xid()
player.set_window_handle(win_id)
    
win.show()

player.set_state(Gst.State.PLAYING)

Gtk.main()