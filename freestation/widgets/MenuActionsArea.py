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

_HAND = Gdk.Cursor.new(Gdk.CursorType.HAND2)

class MenuActionsArea(Gtk.Box):
    def __init__(self, data):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)

        self.button_back = self.build_button(label = 'Atrás', stock = Gtk.STOCK_GO_BACK)
        self.button_forward = self.build_button(label = 'Siguiente', stock = Gtk.STOCK_GO_FORWARD)
        self.button_home = self.build_button(label = 'Inicio', stock = Gtk.STOCK_HOME)
        
        
        self.pack_start(Gtk.Label(), True, True, False)
        self.pack_start(self.button_back, False, False, False)
        self.pack_start(self.button_home, False, False, False)
        self.pack_start(self.button_forward, False, False, False)
        self.pack_start(Gtk.Label(), True, True, False)
        
        self.connect('enter-notify-event', self.on_enter)
        self.connect('leave-notify-event', self.on_leave)
     
    def build_button(self, label = None, stock = None):
        button = Gtk.Button(label, stock)
        button.connect('enter-notify-event', self.on_enter)
        button.connect('leave-notify-event', self.on_leave)
        #button.set_focus_on_click(False)
        return button
        
    def on_enter(self, widget, event):
        window = self.get_window()
        window.set_cursor(_HAND)

    def on_leave(self, widget, event):
        window = self.get_window()
        window.set_cursor(None)