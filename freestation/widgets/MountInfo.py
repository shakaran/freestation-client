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

from freestation.widgets.MountDetector import MountDetector
from freestation.widgets.WhiteLabel import WhiteLabel

class MountInfo(Gtk.Box):
    def __init__(self, data):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)
        
        self.create_progress_bar_text()
        self.create_progress_bar()
        
        mount_detector_widget = MountDetector(self) #@UnusedVariable
        
    def create_progress_bar_text(self):
        self.progress_bar_text = WhiteLabel('Storage: device no detected', angle = 0, halign = Gtk.Align.CENTER)
        self.progress_bar_text.set_size_request(100, -1)
        self.set_margin_top(15)
        self.set_margin_bottom(15)
        
        self.pack_start(self.progress_bar_text, False, False, False)
    
    def create_progress_bar(self):
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_fraction(0)
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_text('-')
        self.progress_bar.set_size_request(100, 30)
        
        self.pack_start(self.progress_bar, False, False, False)
        