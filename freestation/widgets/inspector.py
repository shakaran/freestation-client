#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# userwebkit: so WebKitGtk apps can to talk to a usercouch
# Copyright (C) 2011-2012 Novacut Inc
#
# This file is part of `userwebkit`.
#
# `userwebkit` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `userwebkit` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `userwebkit`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>
#

from gi.repository import Gtk, WebKit #@UnresolvedImport

class Inspector(Gtk.VBox):
    def __init__(self, env, view):
        super().__init__()

        hbox = Gtk.HBox()
        self.pack_start(hbox, False, False, 0)

        close = Gtk.Button(stock=Gtk.STOCK_CLOSE)
        hbox.pack_start(close, False, False, 2)
        close.connect('clicked', self.on_close)

        self.reload = Gtk.Button('Reload')
        hbox.pack_start(self.reload, False, False, 2)

        self.futon = Gtk.Button('CouchDB Futon')
        hbox.pack_start(self.futon, False, False, 2)

        scroll = Gtk.ScrolledWindow()
        self.pack_start(scroll, True, True, 0)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        #self.view = CouchView(env)
        from freestation.widgets.Browser import Browser
        self.view = WebKit.WebView() # view #WebKit.WebView() #Browser()
        scroll.add(self.view)
        self.view.show()

    def on_close(self, button):
        self.destroy()