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
LOG = Logger('ScrolledBox').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import GObject #@UnresolvedImport

class ScrolledBox(Gtk.Box):
    # http://shlomme.diotavelli.net/2009/05/17/scrollable-widgets-with-pygtk/
    __gsignals__ = { 'set-scroll-adjustments' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (Gtk.Adjustment, Gtk.Adjustment)) }
 
    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)

        #self.set_set_scroll_adjustments_signal("set-scroll-adjustments")
        
        #adj = Gtk.Adjustment(0.8, 0.0, 1.0, 0.1, 0.1, 0.1)
        #self.set_scroll_adjustments(adj, adj)