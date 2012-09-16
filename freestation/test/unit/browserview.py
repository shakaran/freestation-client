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

sys.path.append(os.path.dirname(__file__)) #@UndefinedVariable
sys.path.append(os.path.split(os.path.dirname(__file__))[0]) #@UndefinedVariable

from freestation.test.fsunittest import BaseUnitTest
from freestation.widgets.BrowserView import BrowserView

class BrowserViewUnitTest(BaseUnitTest):
    
    def setUp(self):
        self.on_setUp()
        self.browser_view = BrowserView(None)
    
    def tearDown(self):
        self.on_tearDown()
        del self.browser_view
        
    def test_classname(self):
        """ Checks the class instance """
        self.assertEqual(self.browser_view.__class__.__name__, 'BrowserView')
    
    def test_counter(self):
        self.assertIsNotNone(self.browser_view.counter)
        
    def test_view(self):
        self.assertIsNotNone(self.browser_view.view)
    
    def test_view_properties(self):
        """ Checks the view properties """
        view = self.browser_view.view
        
    def test_view_request(self):
        view = self.browser_view.view
        self.assertIsNone(view._on_request(None, None, None, None, None))
        
        # Make sure on_request() immediately returns when env is None:
        self.assertIsNone(
            view._on_nav_policy_decision(None, None, None, None, None)
        )

if __name__ == '__main__':
    try:
        BrowserViewUnitTest.main()
    except SystemExit:
        pass