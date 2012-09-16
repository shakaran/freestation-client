#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# This file is part of FreeStation.
#
# FreeStation is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
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

"""
dpkg -S /usr/bin/gst-inspect-1.0
 gstreamer1.0-tools: /usr/bin/gst-inspect-1.0
 
/usr/bin/gst-inspect-1.0 playbin

dpkg -l '*gst*1.0*'

For debug:

http://wiki.python.org/moin/DebuggingWithGdb

sudo apt-get install libglib2.0-0-dbg gstreamer1.0-plugins-base-dbg libgstreamer-plugins-base1.0-dev libgstreamer-plugins-base1.0-0

LANG=en_US.UTF-8
GST_DEBUG=*:6 gst-launch-1.0 autovideosrc ! autovideosink 2>xvimagesink-debug.lo


sudo gdb gst-launch-1.0 22136

(gdb) thread apply all bt

"""
__author__    = 'Ángel Guzmán Maeso'
__version__   = '$Revision$'
__date__      = '$Date$'
__copyright__ = 'Copyright (c) 2012 Ángel Guzmán Maeso'
__license__   = 'GPL'

import sys

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    print 'Could not find required Gtk 3.0 library.'
    sys.exit(1)
    
try:
    gi.require_version('Gst', '1.0')
except ValueError:
    print 'Could not find required Gstreamer 1.0 library.'
    sys.exit(1)

from gi.repository import GdkX11, Gtk
from gi.repository import Gtk
from gi.repository import Gst, GstVideo
from gi.repository import GObject

GObject.threads_init()

""" This class test message signals members emitted on GStreamer 1.0 for PyGi (GTK 3) """
class Video:

    VIDEO_OGG = 'freestation/ogv/orbit.ogv'
    
    def __init__(self):

        #Gdk.threads_init()
        
        win = Gtk.Window()
        #win.set_resizable(False)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_double_buffered(True)
        win.connect('destroy', self.on_destroy)
        win.connect('delete-event', self.on_delete_event)

        #win.realize()

        # The xid it is only available after realize (also signal realize)
        # It requires import GdkX11 for get_xid() method available
        ####self.xid = win.get_window().get_xid()
        
        ##fixed = Gtk.Fixed()
        
        #for x in dir(fixed):
        #    print x
        
        hbox = Gtk.HBox()
        win.set_size_request(840, 480)
        
        ##fixed.show()

        self.videowidget = Gtk.DrawingArea()
        
        ##fixed.put(self.videowidget, 0, 0)
        #self.videowidget.set_size_request(440, 280)
        #self.videowidget.realize()
        

        #self.videowidget.show()
        ##hbox.pack_start(self.videowidget, True, True, True)
        button = Gtk.Button('Hello')
        button.show()
        
        hbox.pack_start(button, True, True, True)
        hbox.pack_start(self.videowidget, True, True, True)
        
        win.add(hbox)
        win.show_all()
        
        # https://bugzilla.gnome.org/show_bug.cgi?id=663360 Don't use get_window()
        self.xid = self.videowidget.get_property('window').get_xid()
        
        
        # http://bazaar.launchpad.net/~jderose/+junk/gst-examples/view/head:/video-player-1.0
        
        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()
        
        # # Add playbin to the pipeline
        #self.pipeline.add(self.playbin)

        
        self.setup_gstreamer()
        
        self.create_player()
        
        # GstVideo provides GstVideoOverlay with logic for window handle
        # No need to fetch the signal on bus for message::async-start
        self.player.set_window_handle(self.xid)
        
        print 'Auto flush:', self.player.get_auto_flush_bus()
        self.player.set_property('auto-flush-bus' , False) # set_auto_flush_bus()
        print 'Delay:', self.player.get_delay()
        self.player.set_property('delay', 0) # On nanoseconds # set_delay()
        
        #print self.player.bin (field) it should return a GstBin => RuntimeError: unable to get the value
        print self.player.stream_time
        
        # 'NULL', 'PAUSED', 'PLAYING', 'READY', 'VOID_PENDING'
        assert self.set_player_state(Gst.State.NULL) == Gst.StateChangeReturn.SUCCESS # Set player initial state
                 
        self.configure_bus()
        #print Gst.BusSyncReply.DROP # 'ASYNC', 'DROP', 'PASS'
        
        assert self.set_player_state(Gst.State.READY) == Gst.StateChangeReturn.SUCCESS
        
        self.player.set_property('uri', 'file://' + self.VIDEO_OGG) 

        assert self.set_player_state(Gst.State.PLAYING) == Gst.StateChangeReturn.ASYNC

        Gtk.main()

    def setup_gstreamer(self):
                # Setup GStreamer 
        Gst.init(None)
        Gst.init_check(None)
        print Gst.version_string(), Gst.version()

        Gst.debug_set_active(True)
        Gst.debug_print_stack_trace() # If activated, debugging messages are sent to the debugging handlers.
        
        """ 
        COUNT
        DEBUG
        ERROR
        FIXME
        INFO
        LOG
        MEMDUMP
        NONE
        TRACE
        WARNING
        
        Gst.DebugLevel
        """
    
    def create_player(self):
        if Gst.ElementFactory.find('playbin'): # filesrc
            self.player = Gst.ElementFactory.make('playbin', 'MultimediaPlayer')
            #self.player.set_window_handle()
        else:
            print 'Error: could not find the playbin plugin for gstreamer'
            sys.exit(1)
        
        if self.player == None:
            print 'Error: could not create the player'
            sys.exit(1)
        else:
            print '\nLoaded:', self.player.get_name(),
            print 'from', self.player.get_path_string()
            
            print '  Base time:', self.player.get_base_time()
            print '  Control rate:', self.player.get_control_rate()
            print '  Delay:', self.player.get_delay()
            print '  Parent:', self.player.get_parent()
            print '  Start time:', self.player.get_start_time()
            print '  Children:', self.player.numchildren
            print '  Pads:', self.player.numpads
            print '  Sinkpads:', self.player.numsinkpads
            print '  Srcpads:', self.player.numsrcpads
            #print self.player.element # RuntimeError: unable to get the value ??

            factory = self.player.get_factory()
            
            if not factory.get_element_type().name == 'GstPlayBin':
                print 'Error: player is not a GstPlayBin object'
                sys.exit(1)
            if factory.check_version(1, 0, 0): # Check the version for playbin
                print '\n  Loaded factory:', factory.get_name(), # playbin
                print 'from', factory.get_path_string() # /GstRegistry:registry0/GstElementFactory:playbin
            
                print '    Pad templates:', factory.get_num_pad_templates() # 0
                print '    Rank:', factory.get_rank() # 0
                print '    Control rate:', factory.get_control_rate() # 100000000
                #print element.get_uri_protocols() # []
                #print element.get_uri_type() # <enum GST_URI_UNKNOWN of type URIType>
            else:
                print 'Player does not have the required version.'
                sys.exit(1)
            
            self.clock_render()
       
    def set_player_state(self, state):
        result = self.player.set_state(state)

        if result == Gst.StateChangeReturn.SUCCESS:
            print '* Player set the state', state.value_nick, 'with success'
        elif result == Gst.StateChangeReturn.FAILURE:
            print '* Error: player cannot set the state', state
        elif result == Gst.StateChangeReturn.ASYNC:
            print '* Player async the state'
        elif result == Gst.StateChangeReturn.NO_PREROLL:
            print '* NO_PREROLL status', result
        else:
            print '* Unknown result state', result
        
        return result

    def on_sync_handler(self, bus, message):
        print 'on_sync_handler', message
        
    # http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer/html/gstreamer-GstMessage.html#GstMessageType
    def on_message(self, bus, message):
        if message.get_structure():
            if message.get_structure().get_name():
                name = message.get_structure().get_name()
                title = name.title()
                if title != 'Gstmessagestreamstatus' and title != 'Gstmessagenewclock' \
                and title != 'Gstmessageasyncdone'  and title != 'Gstmessagewarning' \
                and title != 'Gstmessageerror' \
                and title != 'Gstmessageqos': # title != 'Gstmessagestate' and title != 'Gstmessagewarning' and 
                    print('message: {!r}'.format(message))
                    print 'Structure:', name
                    print 'Title:', title, ' SEQNUM:', message.get_seqnum()
            else:
                print('message: {!r}'.format(message))
                print 'Structure:', name
                print ' SEQNUM:', message.get_seqnum()
                
                
        else:
            print('message: {!r}'.format(message))
                
            """
                GstMessageError", "GstMessageWarning", "GstMessageInfo",
               "GstMessageBuffering", "GstMessageState", "GstMessageClockProvide",
               "GstMessageClockLost", "GstMessageNewClock", "GstMessageStructureChange",
               "GstMessageSegmentStart", "GstMessageSegmentDone", "GstMessageDuration",
               "GstMessageAsyncStart", "GstMessageRequestState", "GstMessageStreamStatus"
            """
    def on_message_unknown(self, bus, message):
         print 'unknown message received SEQNUM:', message.get_seqnum()
 
    def on_message_tag(self, bus, message):
         print 'tag message received SEQNUM:', message.get_seqnum()
         
    def on_message_toc(self, bus, message):
         print 'toc message received SEQNUM:', message.get_seqnum()
         
    def on_message_info(self, bus, message):
         print 'info message received SEQNUM:', message.get_seqnum()
         
    def on_message_buffering(self, bus, message):
         print 'buffering message received SEQNUM:', message.get_seqnum()
         
    def on_message_state_changed(self, bus, message):
         print 'state changed message received SEQNUM:', message.get_seqnum()       
         
    def on_message_state_dirty(self, bus, message):
         print 'state dirty message received SEQNUM:', message.get_seqnum()
                
    def on_message_step_done(self, bus, message):
         print 'step done message received SEQNUM:', message.get_seqnum()
         
    def on_message_clock_provide(self, bus, message):
         print 'clock provide message received SEQNUM:', message.get_seqnum() 
                 
    def on_message_clock_lost(self, bus, message):
         print 'clock lost message received SEQNUM:', message.get_seqnum()
               
    def on_message_structure_change(self, bus, message):
         print 'structure change message received SEQNUM:', message.get_seqnum() 
         
    def on_message_segment_start(self, bus, message):
         print 'segment start message received SEQNUM:', message.get_seqnum()
          
    def on_message_segment_done(self, bus, message):
         print 'segment done message received SEQNUM:', message.get_seqnum()
          
    def on_message_duration(self, bus, message):
         print 'duration message received SEQNUM:', message.get_seqnum()
          
    def on_message_latency(self, bus, message):
         print 'latency message received SEQNUM:', message.get_seqnum()
         
    def on_message_async_start(self, bus, message):
         print 'async start message received SEQNUM:', message.get_seqnum()
         
    def on_message_request_state(self, bus, message):
         print 'request state message received SEQNUM:', message.get_seqnum()
         
    def on_message_step_start(self, bus, message):
         print 'step start message received SEQNUM:', message.get_seqnum()
         
    def on_message_progress(self, bus, message):
         print 'progress message received SEQNUM:', message.get_seqnum()
                                                               
    def on_message_application(self, bus, message):
         print 'application message received SEQNUM:', message.get_seqnum()
         
    def on_message_any(self, bus, message):
         print 'any message received SEQNUM:', message.get_seqnum()
                                      
    def on_message_state(self, bus, message):
         print 'Status message received SEQNUM:', message.get_seqnum()
         
    def on_message_warning(self, bus, message):
         print 'Warning message received SEQNUM:', message.get_seqnum()

    def on_message_new_clock(self, bus, message):
         print 'New clock message received SEQNUM:', message.get_seqnum()
         print message.parse_qos() # GStreamer-CRITICAL **: gst_message_parse_qos: assertion `GST_MESSAGE_TYPE (message) == GST_MESSAGE_QOS' failed
         #(False, 0L, 0L, 0L, 0L)
         print message.parse_qos_stats() # GStreamer-CRITICAL **: gst_message_parse_qos_stats: assertion `GST_MESSAGE_TYPE (message) == GST_MESSAGE_QOS' failed
         #(<enum GST_FORMAT_UNDEFINED of type Format>, 0L, 0L)
         print message.parse_qos_values() # GStreamer-CRITICAL **: gst_message_parse_qos_values: assertion `GST_MESSAGE_TYPE (message) == GST_MESSAGE_QOS' failed
         print message.parse_request_state() # GStreamer-CRITICAL **: gst_message_parse_request_state: assertion `GST_MESSAGE_TYPE (message) == GST_MESSAGE_REQUEST_STATE' failed
         #<enum GST_STATE_VOID_PENDING of type State>
         
    def on_message_async_done(self, bus, message):
         print 'Async done message received SEQNUM:', message.get_seqnum()
                
    def on_message_stream_status(self, bus, message):
         print 'Stream state message received SEQNUM:', message.get_seqnum()
         
    def on_message_qos(self, bus, message):
         print 'QOS status message received SEQNUM:', message.get_seqnum()
         
    def on_message_element(self, bus, message):
         print 'message element received SEQNUM:', message.get_seqnum()
         
    def on_message_eos(self, bus, message):
        # End of Stream 
        print 'EOS message received SEQNUM:', message.get_seqnum()
        # on_eos(): seeking to start of video
        self.player.seek_simple(
            Gst.Format.TIME,        
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )
        #self.set_player_state(Gst.State.NULL)
        #self.on_destroy(None)

    def on_message_error(self, bus, message):
        """ Unexpected error """
        self.set_player_state(Gst.State.NULL)
        
        error = message.parse_error()[1]
        print error
        
        print '\n\nError message received. Aborting.'
        if message.type == Gst.MessageType.ERROR:
            print 'Secuence number:', message.get_seqnum(), 'at', message.timestamp
            print 'Object:', message.src.__class__.__name__
            print 'Quark:', message.type_to_quark(message.type),
            print '(' + message.type_get_name(message.type) + ')'
            
            print 'First value:', message.type.first_value_name, #'first_value_name', 'first_value_nick', 'imag', 'numerator', 'real', 'value_names', 'value_nicks']
            print '(' + message.type.first_value_nick + ')'
            print 'Imag', message.type.imag
            print 'Numerator:', message.type.numerator
            print 'Real:', message.type.real
            print 'Other values:', message.type.value_names
            print 'Other values nicks:', message.type.value_nicks
            
            # 'parse_error', 'parse_info'
        
        message.unref() # Explicitily free memory
        sys.exit(1)


    """
    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            xid = self.drawingarea.get_property('window').get_xid()
            msg.src.set_window_handle(xid)
    """
    
    def on_sync_message(self, bus, message):
        """ Message is recieved and  signal is emitted here """
        
        print 'Secuence number:', message.get_seqnum()
        structure = message.get_structure()
       
        if structure is None: 
            return False 
       
        structure_name = structure.get_name()

        if structure_name == 'playbin-stream-changed':
            pass
        elif structure_name == 'prepare-window-handle':
            imagesink = message.src 
            print 'Image sink have', imagesink
        elif structure_name == 'have-window-handle': #"prepare-xwindow-id":
            if sys.platform == "win32":
                win_id = self.videowidget.get_window().get_handle()
            else:
                win_id = self.videowidget.get_window().get_xid()
            assert win_id
            
            print 'Win ID', win_id
            
            #Gdk.threads_init()
            #Gdk.flush() # Flushes the X output buffer and waits until all requests have been processed by the server. Avoid gdk_error_trap errors
            #Gdk.threads_enter()
            Gdk.Display().get_default().sync()
            # GstXvImageSink http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-xvimagesink.html
            imagesink = message.src 
            print imagesink
            factory = imagesink.get_factory()
            print '\n  Loaded factory:', factory.get_name(), # xvimagesink
            print 'from', factory.get_path_string() # /GstRegistry:registry0/GstElementFactory:xvimagesink
            print dir(factory)
            
            # http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-base-plugins/html/gst-plugins-base-plugins-xvimagesink.html
            print 'force-aspect-ratio', imagesink.get_property('force-aspect-ratio')
            print 'double-buffer', imagesink.get_property('double-buffer')
            print 'brightness', imagesink.get_property('brightness')
            print 'contrast', imagesink.get_property('contrast')
            print 'display', imagesink.get_property('display')
            print 'hue', imagesink.get_property('hue')
            print 'pixel-aspect-ratio', imagesink.get_property('pixel-aspect-ratio')
            print 'saturation', imagesink.get_property('saturation')
            print 'synchronous', imagesink.get_property('synchronous')
            print 'saturation', imagesink.get_property('saturation')
            print 'device', imagesink.get_property('device')
            print 'device-name', imagesink.get_property('device-name')
            print 'handle-events', imagesink.get_property('handle-events')
            print 'handle-expose', imagesink.get_property('handle-expose')
            print 'autopaint-colorkey', imagesink.get_property('autopaint-colorkey')
            print 'handle-expose', imagesink.get_property('handle-expose')
            print 'colorkey', imagesink.get_property('colorkey')
            print 'draw-borders', imagesink.get_property('draw-borders')
            print 'window-height', imagesink.get_property('window-height')
            print 'window-width', imagesink.get_property('window-width')
            
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_property('double-buffer', True) #Gdk-WARNING **: XSetErrorHandler() called with a GDK error trap pushed. Don't do that.
            imagesink.set_property('double-buffer', True)
            
            print dir(imagesink)
            """
              "brightness"               gint                  : Read / Write
              "contrast"                 gint                  : Read / Write
              "display"                  gchar*                : Read / Write
              "hue"                      gint                  : Read / Write
              "pixel-aspect-ratio"       gchar*                : Read / Write
              "saturation"               gint                  : Read / Write
              "synchronous"              gboolean              : Read / Write
              "force-aspect-ratio"       gboolean              : Read / Write
              "device"                   gchar*                : Read / Write
              "device-name"              gchar*                : Read
              "handle-events"            gboolean              : Read / Write
              "double-buffer"            gboolean              : Read / Write
              "handle-expose"            gboolean              : Read / Write
              "autopaint-colorkey"       gboolean              : Read / Write
              "colorkey"                 gint                  : Read / Write
              "draw-borders"             gboolean              : Read / Write
              "window-height"            guint64               : Read
              "window-width"             guint64               : Read
            """
            print 'ImageSink', dir(imagesink)
            self.player.set_window_handle(win_id)
            #imagesink.set_xwindow_id(win_id) 
            #Gdk.threads_leave()
        else:
            print 'Message', dir(structure)
            print 'Structure:', dir(structure)
            print 'Message: ', structure_name, '(no intercepted)'
    
    def configure_bus(self):
        """ The bus allows applications to receive GstMessage packets """
        self.bus = self.player.get_bus() 
        print '\nLoaded factory:', self.bus.get_name(), # bus
        print 'from', self.bus.get_path_string() # /GstBus:bus1

        self.bus.add_signal_watch() 
        self.bus.enable_sync_message_emission() 
        
        #for x in dir(Gst.Message.new_element(bus, Gst.Structure)): 
        #    print x
        #bus.sync_signal_handler(Gst.Message.ELEMENT, None)
        #for x in dir(self.bus):
        #    print x

        #used to get messages that GStreamer emits 
        """
          <member name="unknown" value="0" c:identifier="GST_MESSAGE_UNKNOWN"/>
          <member name="eos" value="1" c:identifier="GST_MESSAGE_EOS"/>
          <member name="error" value="2" c:identifier="GST_MESSAGE_ERROR"/>
          <member name="warning" value="4" c:identifier="GST_MESSAGE_WARNING"/>
          <member name="info" value="8" c:identifier="GST_MESSAGE_INFO"/>
          <member name="tag" value="16" c:identifier="GST_MESSAGE_TAG"/>
          <member name="buffering"
                  value="32"
                  c:identifier="GST_MESSAGE_BUFFERING"/>
          <member name="state_changed"
                  value="64"
                  c:identifier="GST_MESSAGE_STATE_CHANGED"/>
          <member name="state_dirty"
                  value="128"
                  c:identifier="GST_MESSAGE_STATE_DIRTY"/>
          <member name="step_done"
                  value="256"
                  c:identifier="GST_MESSAGE_STEP_DONE"/>
          <member name="clock_provide"
                  value="512"
                  c:identifier="GST_MESSAGE_CLOCK_PROVIDE"/>
          <member name="clock_lost"
                  value="1024"
                  c:identifier="GST_MESSAGE_CLOCK_LOST"/>
          <member name="new_clock"
                  value="2048"
                  c:identifier="GST_MESSAGE_NEW_CLOCK"/>
          <member name="structure_change"
                  value="4096"
                  c:identifier="GST_MESSAGE_STRUCTURE_CHANGE"/>
          <member name="stream_status"
                  value="8192"
                  c:identifier="GST_MESSAGE_STREAM_STATUS"/>
          <member name="application"
                  value="16384"
                  c:identifier="GST_MESSAGE_APPLICATION"/>
          <member name="element" value="32768" c:identifier="GST_MESSAGE_ELEMENT"/>
          <member name="segment_start"
                  value="65536"
                  c:identifier="GST_MESSAGE_SEGMENT_START"/>
          <member name="segment_done"
                  value="131072"
                  c:identifier="GST_MESSAGE_SEGMENT_DONE"/>
          <member name="duration"
                  value="262144"
                  c:identifier="GST_MESSAGE_DURATION"/>
          <member name="latency"
                  value="524288"
                  c:identifier="GST_MESSAGE_LATENCY"/>
          <member name="async_start"
                  value="1048576"
                  c:identifier="GST_MESSAGE_ASYNC_START"/>
          <member name="async_done"
                  value="2097152"
                  c:identifier="GST_MESSAGE_ASYNC_DONE"/>
          <member name="request_state"
                  value="4194304"
                  c:identifier="GST_MESSAGE_REQUEST_STATE"/>
          <member name="step_start"
                  value="8388608"
                  c:identifier="GST_MESSAGE_STEP_START"/>
          <member name="qos" value="16777216" c:identifier="GST_MESSAGE_QOS"/>
          <member name="progress"
                  value="33554432"
                  c:identifier="GST_MESSAGE_PROGRESS"/>
          <member name="toc" value="67108864" c:identifier="GST_MESSAGE_TOC"/>
          <member name="any" value="-1" c:identifier="GST_MESSAGE_ANY"/>
        """

        self.bus.connect('message::state', self.on_message_state)  # No works
        
        self.bus.connect('message', self.on_message)
        self.bus.connect('message::unknown', self.on_message_unknown)
        self.bus.connect('message::eos', self.on_message_eos)
        self.bus.connect('message::error', self.on_message_error)
        self.bus.connect('message::warning', self.on_message_warning) # No works
        self.bus.connect('message::info', self.on_message_info)
        self.bus.connect('message::tag', self.on_message_tag)
        self.bus.connect('message::buffering', self.on_message_buffering)
        self.bus.connect('message::state-changed', self.on_message_state_changed)
        self.bus.connect('message::state-dirty', self.on_message_state_dirty)
        self.bus.connect('message::step-done', self.on_message_step_done)
        self.bus.connect('message::clock-provide', self.on_message_clock_provide)
        self.bus.connect('message::clock-lost', self.on_message_clock_lost)
        self.bus.connect('message::new-clock', self.on_message_new_clock)
        self.bus.connect('message::structure-change', self.on_message_structure_change)
        self.bus.connect('message::stream-status', self.on_message_stream_status)
        self.bus.connect('message::element', self.on_message_element)
        self.bus.connect('message::application', self.on_message_application)
        self.bus.connect('message::segment-start', self.on_message_segment_start)
        self.bus.connect('message::segment-done', self.on_message_segment_done)
        self.bus.connect('message::duration', self.on_message_duration)
        self.bus.connect('message::latency', self.on_message_latency)
        self.bus.connect('message::async-start', self.on_message_async_start)
        self.bus.connect('message::async-done', self.on_message_async_done)
        self.bus.connect('message::request-state', self.on_message_request_state)
        self.bus.connect('message::step-start', self.on_message_step_start)
        self.bus.connect('message::qos', self.on_message_qos)
        self.bus.connect('message::progress', self.on_message_progress)
        self.bus.connect('message::toc', self.on_message_toc)
        self.bus.connect('message::any', self.on_message_any)
        
        ##self.bus.sync_signal_handler(self.on_sync_handler, Gst.Message.new_element(self.bus, Gst.Structure()))
        
        #used for connecting video to your application 
        self.bus.connect('sync-message::element', self.on_sync_message)
    
    def clock_render(self):
        """ 
            http://developer.gnome.org/gstreamer/unstable/GstSystemClock.html 
            http://developer.gnome.org/gstreamer/unstable/GstClock.html
        """
        player_clock = self.player.get_clock() # Gets the current clock used by pipeline.

        system_clock = player_clock.obtain() # SystemClock 
        #print system_clock.clock # (RuntimeError: unable to get the value)
        #print system_clock.clock-type # (RuntimeError: unable to get the value)
        #print system_clock.realtime # AttributeError: 'SystemClock' object has no attribute 'realtime'
        #print system_clock.monotonic # AttributeError: 'SystemClock' object has no attribute 'monotonic'
        

        #print player_clock.clock # RuntimeError: unable to get the value

        print '\nLoaded:', player_clock.get_name(),
        print 'from', player_clock.get_path_string()
           
        #print 'Clock type:', player_clock.clock-type
        #print '  Realtime:', player_clock.realtime
        #print '  Monotonic:', player_clock.monotonic
        print '  Calibration:', player_clock.get_calibration()
        print '  Control rate:', player_clock.get_control_rate()
        print '  Resolution:', player_clock.get_resolution()
        print '  Current time:', player_clock.get_time()
        print '  Internal time:', player_clock.get_internal_time()
        print '  Timeout:', player_clock.get_timeout()
        print '  Master:', player_clock.get_master(), '\n'
    
    def on_delete_event(self, widget, event):
        print 'on delete event', widget, event
    
    def on_destroy(self, widget):
        print 'destroy', widget
        if self.player:
            self.set_player_state(Gst.State.NULL)
            del self.player
            
        if Gtk.main_level() > 0:
            Gtk.main_quit()
        
if __name__ == '__main__':
    Video()