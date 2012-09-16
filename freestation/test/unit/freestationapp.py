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

import sys, os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.split(os.path.dirname(__file__))[0])

from freestation.test.fsunittest import BaseUnitTest
from freestation.freestationapp import FreeStationApp

class FreeStationAppTest(BaseUnitTest):
    
    def setUp(self):
        self.on_setUp()
        self.freestationapp = FreeStationApp()
    
    def tearDown(self):
        self.on_tearDown()
        del self.freestationapp
        
    def test_classname(self):
        ''' Checks the class instance '''
        self.assertEqual(self.freestationapp.__class__.__name__, 'FreeStationApp')
        
    """def test_launch(self):
        ''' Test a launch without GUI '''
        self.assertEquals(self.freestationapp.launch(self.ALIVE_TIME, False), None)
    """    
if __name__ == '__main__':
    try:
        FreeStationAppTest.main()
    except SystemExit:
        pass