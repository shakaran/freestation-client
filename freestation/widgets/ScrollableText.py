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

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from freestation.widgets.WhiteLabel import WhiteLabel

class ScrollableText(Gtk.ScrolledWindow):
    __gtype_name__ = 'ScrollableText'
    __name__ = 'ScrollableText' #@ReservedAssignment
    
    DEFAULT_BACKGROUND   = '#660707'
    
    DEFAULT_COLOR   = '#ffffff'
    
    def __init__(self, text):
        Gtk.ScrolledWindow.__init__(self)
        
        self.label = WhiteLabel(text)
        self.label.set_alignment(xalign=0, yalign=0)
        self.label.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#800000"))
        
        self.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        self.add_with_viewport(self.label) 
        self.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.set_size_request(400, 600)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
            
