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

import tempfile
import cProfile

(fileno, filename) = tempfile.mkstemp()

def run():
    import os
    if os.path.exists('webkit.lock'):
        os.remove('webkit.lock')
        
    import time
    from freestationapp import FreeStationApp
    
    app = FreeStationApp(3, True)
    app.setName('FreeStation' + '-' + str(time.time()))
    app.start()
    app.run()

cProfile.run('run()', filename)

import pstats
p = pstats.Stats(filename)
p.sort_stats('cumulative').print_stats(40)
