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

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport

class TitleDisplay(Gtk.Label):
    """
        Create a widget based on Gtk.Lable for custom titles
    """
    
    DEFAULT_TEXT_SIZE = 48
    DEFAULT_BACKGROUND = '#a22b2b'
    DEFAULT_COLOR      = '#9C132E'
    
    def __init__(self):
        Gtk.Label.__init__(self, None) # Empty label
        
        self.size = self.DEFAULT_TEXT_SIZE
        self.background = self.DEFAULT_BACKGROUND
        
    
    def getTextDirection(self):
        """ Get the direction of text:
            - LTR: Left-To-Right direction
                Gtk.TextDirection.LTR
            - RTL: Right-To-Left direction
                Gtk.TextDirection.RTL
            
            By default LTR
        """
        return Gtk.TextDirection.LTR
    
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
        self.set_markup('<span rise="0" font_family="serif" letter_spacing="10" font = "{0}" weight = "bold">{1}</span>'.format(self.size, self.data))
        #self.set_alignment(0.0, 0.5)
        
        #for x in dir(self):
        #    print x
        
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))
        self.set_margin_bottom(0)
        self.set_margin_left(0)
        self.set_margin_right(0)
        self.set_margin_top(0)
        self.set_hexpand(0)
        self.set_vexpand(0)
        self.set_size_request(150, 300)
        layout = self.get_layout()
        print ('Layour height: ' + str(layout.get_height()))
        print ('Layour height: ' + str(layout.get_spacing()))
        print (layout.get_size())
        layout.set_height(10)
        layout.set_spacing(0) 
        #print 