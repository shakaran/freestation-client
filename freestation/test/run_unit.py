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

import unittest, logging, sys

from freestation import __version__ as version

from freestation.test.unit import freestationapp
from freestation.test.unit import watchdog
from freestation.test.unit import browserview

# Gets the instance of the logger.
logSys = logging.getLogger("freestation")
# Add the default logging handler
stdout = logging.StreamHandler(sys.stdout)
logSys.addHandler(stdout)
logSys.setLevel(logging.FATAL)

print "FreeStation " + str(version) + " test suite. Please wait..."

tests = unittest.TestSuite()

# Filter
tests.addTest(unittest.makeSuite(freestationapp.FreeStationAppTest))
tests.addTest(unittest.makeSuite(watchdog.WatchdogUnitTest))
tests.addTest(unittest.makeSuite(browserview.BrowserViewUnitTest))

# Tests runner
testRunner = unittest.TextTestRunner()
testRunner.run(tests)