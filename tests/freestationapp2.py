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

import gi
try:
    gi.require_version('Gtk', '3.0')
except ValueError:
    print ('Could not find required Gtk 3.0 library. Aborting.')
    sys.exit(1)

from gi.repository import Gtk, Gdk, GObject #@UnresolvedImport
from constants import APP_NAME #@UnresolvedImport
from threading import Thread, Condition

from logger import Logger #@UnresolvedImport
LOG = Logger('FreeStationApp').get()

class FreeStationApp2(object):
    
    __name__ = APP_NAME #@ReservedAssignment
    
    # Class variable referring to the one and only app for use
    _self = None
    
    def __init__(self, alive_time = None, enable_gui = True):
        """
            @param alive_time msec for live app, normally used by test. Default None for ignore
        """
        #Thread.__init__(self)
        #self.setDaemon(True) 
        self.finished = False
        
        if FreeStationApp2._self != None:
            raise RuntimeError('Only a single instance of a FreeStationApp can be instantiated.')
        
        FreeStationApp2._self = self

    def run(self, ):
        LOG.debug('Parent PID: {0}'.format(os.getppid()))
        LOG.debug('FreeStationApp PID: {0}'.format(os.getpid()))
        #LOG.debug('Thread name: {0}'.format(self.getName()))

        GObject.threads_init()

        Gdk.threads_enter()    
        from widgets.webkitview import App #@UnresolvedImport
        self.gui = App(self)
        self.gui.show_html()
            #self.gui.run()
        Gdk.threads_leave()
  
        Gdk.threads_enter()    
        Gtk.main()
        Gdk.threads_leave()
    
    # Destroy the object. Wait for the thread to terminate and cleanup
    # the internal state.
    def destroy(self):
        # Wait for the thread to terminate
        Gdk.threads_leave()
        FreeStationApp2._self = None
        from signal import SIGTERM

        self.finished = True

                  
    def on_destroy(self, widget, event):
        LOG.debug('Destroying application')
        LOG.debug('Parent PID: {0}'.format(os.getppid()))
        LOG.debug('FreeStationApp PID: {0}'.format(os.getpid()))

        Gtk.main_quit()
        if Gtk.main_level() > 0:
            Gtk.main_quit()
            
        self.destroy()