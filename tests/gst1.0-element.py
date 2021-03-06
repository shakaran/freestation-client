#!/usr/bin/python3

from gi.repository import GObject
GObject.threads_init()

import gi
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer 1.0 library.'
    sys.exit(1)
    
from gi.repository import Gst

Gst.init(None)

mainloop = GObject.MainLoop()
pipeline = Gst.Pipeline()

def on_eos(bus, msg):
    print('eos: {!r}'.format(msg))
    pipeline.set_state(Gst.State.NULL)
    mainloop.quit()

def on_message(bus, msg):
    print('message: {!r}'.format(msg))

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect('message::eos', on_eos)
bus.connect('message', on_message)

bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect('message::eos', on_eos)

src = Gst.ElementFactory.make('videotestsrc', None)
src.set_property('num-buffers', 10)
sink = Gst.ElementFactory.make('fakesink', None)
pipeline.add(src)
pipeline.add(sink)
src.link(sink)

pipeline.set_state(Gst.State.PLAYING)
mainloop.run()