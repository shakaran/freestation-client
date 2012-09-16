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

import sys, os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.split(os.path.dirname(__file__))[0])
sys.path.append('/usr/local/lib/python3.2/dist-packages')

from logger import Logger #@UnresolvedImport
LOG = Logger('FreeStationApp').get()

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    print ('Could not find required Gtk 3.0 library. Aborting.')
    sys.exit(1)

from gi.repository import Gtk, Gdk, GObject #@UnresolvedImport
from constants import APP_NAME #@UnresolvedImport
from threading import Thread, Condition

class FreeStationApp(Thread):
    __gtype_name__ = 'FreeStationApp'
    __name__ = APP_NAME #@ReservedAssignment
    
    # Class variable referring to the one and only app for use
    _self = None
    
    def __init__(self, alive_time = None, enable_gui = True):
        """
            @param alive_time msec for live app, normally used by test. Default None for ignore
        """
        Thread.__init__(self)
        #self.setDaemon(True)
        
        if FreeStationApp._self != None:
            raise RuntimeError('Only a single instance of a FreeStationApp can be instantiated.')
        
        FreeStationApp._self = self
        
        # State variables. These are not class static variables.
        self._condition = Condition()
        self._done = False
        
        self.alive_time = alive_time
        self.enable_gui = enable_gui

    def run(self):
        LOG.debug('Parent PID: {0}'.format(os.getppid()))
        LOG.debug('FreeStationApp PID: {0}'.format(os.getpid()))
        LOG.debug('Thread name: {0}'.format(self.getName()))

        GObject.threads_init()
        Gdk.threads_init()
        
        Gdk.flush()
        Gdk.threads_enter()
        
        if self.alive_time:
            print ('Use alive time')
            GObject.timeout_add(self.alive_time, self.on_destroy, None, None)
        
        if self.enable_gui:
            from widgets.GUI import GUI #@UnresolvedImport
            self.gui = GUI(self)
            
        Gtk.main()
        Gdk.threads_leave()
    
        FreeStationApp._self = None
        self._stop()
        
        return
    
    # Destroy the object. Wait for the thread to terminate and cleanup
    # the internal state.
    def destroy(self):
        self._condition.acquire()
        self._done = True
        self._condition.notify()
        self._condition.release()
        
        # Wait for the thread to terminate
        try:
            self.join()
        except RuntimeError:
            # If fails for "thread aliens" skip
            # http://docs.python.org/library/threading.html#thread-objects
            pass
        
        Gdk.threads_leave()
        FreeStationApp._self = None
    
        self._stop()
        return
                  
    def on_destroy(self, widget, event):
        LOG.debug('Destroying application')
        LOG.debug('Parent PID: {0}'.format(os.getppid()))
        LOG.debug('FreeStationApp PID: {0}'.format(os.getpid()))
        LOG.debug('Thread name: {0}'.format(self.getName()))

        if Gtk.main_level() > 0:
            Gtk.main_quit()
            
        self.destroy()

if __name__ == '__main__':
    GObject.threads_init()
    Gdk.threads_init()
        
    import os
    if os.path.exists('webkit.lock'):
        os.remove('webkit.lock')
        
    import time
    app = FreeStationApp(None, True)
    app.setName('FreeStation' + '-' + str(time.time()))
    app.start()
    app.run()
    
    app.__stop()