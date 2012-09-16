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
LOG = Logger('LogoArea').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from gi.repository import GdkPixbuf #@UnresolvedImport

from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

class LogoArea(Gtk.Box):
    __gtype_name__ = 'LogoArea'
    __name__       = 'LogoArea'
    
    DEFAULT_BORDER_WIDTH = 25
    DEFAULT_WIDTH  = 200
    DEFAULT_HEIGHT = 200
    DEFAULT_LOGO   = 'fs-logo.png'
    DEFAULT_BACKGROUND = '#acacac'
    
    def __init__(self, data = None):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)
        self.logo = data
        
        self.border_width = self.DEFAULT_BORDER_WIDTH
        self.width  = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.background = self.DEFAULT_BACKGROUND
    
    def start(self):
        self.set_border_width(self.border_width)
        self.set_logo(self.logo)

    def set_properties(self, properties):
        #print properties
        
        for (key, value) in properties:
            if key == 'position':
                self.position = value
            elif key == 'width':
                self.width = value
            elif key == 'height':
                self.height = value
            elif key == 'border_width':
                self.border_width = value
            elif key == 'data':
                self.data = value
        
    def set_logo(self, logo):
        if not logo:
            if not self.logo:
                self.logo = self.DEFAULT_LOGO
        else:
            self.logo = logo
                
        try:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(join('img', self.logo))
        except:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(join(file_path, 'img', self.logo))
            
        self.fs_logo = Gtk.Image()
        self.fs_logo.set_from_pixbuf(self.icon)
        self.pack_start(self.fs_logo, False, False, False)
        self.set_size_request(int(self.width), int(self.height))
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))