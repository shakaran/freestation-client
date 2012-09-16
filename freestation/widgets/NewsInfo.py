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
LOG = Logger('NewsInfo').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from gi.repository import GdkPixbuf #@UnresolvedImport

from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

class NewsInfo(Gtk.Box):
    __gtype_name__ = 'NewsInfo'
    __name__       = 'NewsInfo'
    
    DEFAULT_BORDER_WIDTH = 25
    DEFAULT_WIDTH  = 200
    DEFAULT_HEIGHT = 200
    DEFAULT_BACKGROUND = '#acacac'
    NEWS_ICON = 'news_icon.png'
    
    def __init__(self, data = None):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)
        
        self.border_width = self.DEFAULT_BORDER_WIDTH
        self.width  = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        self.background = self.DEFAULT_BACKGROUND
    
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
                
    def start(self):
        self.set_border_width(self.border_width)
        
        try:
            self.news_icon = GdkPixbuf.Pixbuf.new_from_file(join('img', self.NEWS_ICON))
        except:
            self.news_icon = GdkPixbuf.Pixbuf.new_from_file(join(file_path, 'img', self.NEWS_ICON))
        
        self.news_icon = self.news_icon.scale_simple(32, 32, GdkPixbuf.InterpType.BILINEAR)
        
        self.news_image = Gtk.Image()
        self.news_image.set_from_pixbuf(self.news_icon)
        
        self.label = Gtk.Label()
        self.label.set_justify(Gtk.Justification.LEFT) 
        self.label.set_markup('<span color="{0}">{1}</span>'.format('#ffffff', 'Novedades'))
        self.label.set_selectable(False)
        self.label.set_margin_bottom(15)
                
        from freestation.widgets.BrowserView import BrowserView
        self.browser_view_widget = BrowserView(None)
        self.browser_view_widget.load('http://youdomain.com/news.php')
        
        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.hbox.pack_start(self.news_image, expand = False, fill = False, padding = 0)
        self.hbox.pack_start(self.label, expand = False, fill = False, padding = 0)
        
        self.pack_start(self.hbox, expand = False, fill = False, padding = 5)
        self.pack_start(self.browser_view_widget, expand = False, fill = False, padding = 0)
      