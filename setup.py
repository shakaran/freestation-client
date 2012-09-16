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

from setuptools import setup, find_packages
from sys import argv
from glob import glob

import freestation

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'freestation server ice'

longdesc = '''
FreeStation'''

setup(
    name             = 'freestation',
    version          = freestation.__version__,
    description      = 'FreeStation',
    long_description = longdesc,
    author           = freestation.__author__,
    author_email     = freestation.__author_email__,
    url              = 'https://github.com/shakaran/freestation',
    packages         = find_packages(),
    download_url     = "http://pypi.python.org/pypi/freestation/",
    classifiers      = CLASSIFIERS,
    keywords         = KEYWORDS,
    zip_safe         = True,
    install_requires = ['distribute'],
    platforms        = 'Posix', 
    license          = 'AGPLv3', 
    """scripts =    [
                    
                ],
    data_files =    [
                    ]"""
)

# Update config file
if argv[1] == 'install':
    print
    print 'Please do not forget to update your configuration files.'
    print