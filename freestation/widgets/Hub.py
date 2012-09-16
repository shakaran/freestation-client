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
from gi.repository import GObject #@UnresolvedImport

import json

def iter_gsignals(signals):
    assert isinstance(signals, dict)
    for (name, argnames) in signals.items():
        assert isinstance(argnames, list)
        args = [GObject.TYPE_PYOBJECT for argname in argnames]
        yield (name, (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, args))
        
def hub_factory(signals):
    print ('hub_factory callback')
    if signals:
        class FactoryHub(Hub):
            __gsignals__ = dict(iter_gsignals(signals))
        return FactoryHub
    return Hub

class Hub(GObject.GObject):
    def __init__(self, view):
        super().__init__()
        self._view = view
        
        # Key aspect, send via notify::title to view the recieved data
        view.set_recv(self.recv)

    def recv(self, data):
        try:
            obj = json.loads(data)
            print ('Hub event=recv:' + str(obj))
            
            if obj['args'] == None:
                self.emit(obj['signal'], None)
            else:
                self.emit(obj['signal'], *obj['args'])
        except ValueError:
            pass

    def send(self, signal, *args):
        """
        Emit a signal by calling the JavaScript Signal.recv() function.
        """
        
        print ('Hub event=send signal=' + str(signal))
        
        script = 'Hub.recv({!r})'.format(
            json.dumps({'signal': signal, 'args': args})
        )
        
        print ('Executing javascript:\n' + script)
        
        self._view.execute_script(script)
        self.emit(signal, *args)   