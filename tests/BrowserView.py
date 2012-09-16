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
LOG = Logger('BrowserView').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk,GObject #@UnresolvedImport

import os

file_path = str(os.path.split(os.path.dirname(__file__))[0])

class BrowserView(Gtk.VPaned):
    
    def __init__(self, data):
        Gtk.VPaned.__init__(self)
        self.counter = 0
        
        self.set_size_request(900, -1)

        print ('Calling to create_browser_scrolled', self.counter)
        self.counter += 1
        
        if self.counter <= 1:
            self.__create_browser_scrolled()

    def __create_browser_scrolled(self):
        Gdk.flush()
        from freestation.widgets.Browser import Browser

        self.view = Browser()
        self.view.connect('render-finished', self.on_render_finished)
        self.view.show()
        
        vbox = Gtk.VBox(False, 5)
        vbox.pack_start(self.view, True, True, 0)
        
        self.pack1(vbox, True, True)
        
    
    def __load_splash(self):
        try:
            splash = open('templates/splash.html', 'r').read() # Eclipse path
        except IOError:
            splash = open(file_path + '/templates/splash.html', 'r').read()

        self.view.load_uri('http://www.uclm.es')
    
    def load(self, url = 'http://www.uclm.es'):
        self.view.load_uri(url)
    
    def on_render_finished(self, view):
        print ('Render finished on BrowserView')
        Gdk.flush()
         
    def on_destroy(self):
        print ('On destroy BrowserView')
        
        if self.view.inspector:
            self.view.inspector.destroy()