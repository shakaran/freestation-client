#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# microfiber: fabric for a lightweight Couch
# Copyright (C) 2011-2012 Novacut Inc
#
# This file is part of `microfiber`.
#
# `microfiber` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `microfiber` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `microfiber`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>
#

# http://bazaar.launchpad.net/~microfiber/microfiber/trunk/view/head:/benchmark_microfiber.py
import time
import platform
import json
import optparse
from subprocess import check_call

from usercouch.misc import TempCouch
import microfiber

name = 'test_benchmark_microfiber'
count = 2000
keys = 50


parser = optparse.OptionParser()
parser.add_option('--oauth',
    help='configure TempCouch with oauth',
    action='store_true',
    default=False,
)
(options, args) = parser.parse_args()


tmpcouch = TempCouch()
auth = ('oauth' if options.oauth else 'basic')
env = tmpcouch.bootstrap(auth)
print('\nenv = {!r}\n'.format(env))
db = microfiber.Database(name, env)
db.put(None)
time.sleep(3)  # Let CouchDB settle a moment
check_call(['/bin/sync'])  # Flush any pending IO so test is more consistent

master = dict(
    ('a' * i, 'b' * i) for i in range(1, keys)
)
ids = tuple(microfiber.random_id() for i in range(count))
docs = []
total = 0

print('*** Benchmarking microfiber ***')
print('Python: {}, {}, {}'.format(
    platform.python_version(), platform.machine(), platform.system())
)

print('  Saving {} documents in db {!r}...'.format(count, name))
start = time.time()
for _id in ids:
    doc = dict(master)
    doc['_id'] = _id
    db.save(doc)
    docs.append(doc)
elapsed = time.time() - start
total += elapsed
print('    Seconds: {:.2f}'.format(elapsed))
print('    Saves per second: {:.1f}'.format(count / elapsed))

print('  Getting {} documents from db {!r}...'.format(count, name))
start = time.time()
for _id in ids:
    db.get(_id)
elapsed = time.time() - start
total += elapsed
print('    Seconds: {:.2f}'.format(elapsed))
print('    Gets per second: {:.1f}'.format(count / elapsed))

print('  Deleting {} documents from db {!r}...'.format(count, name))
start = time.time()
for doc in docs:
    db.delete(doc['_id'], rev=doc['_rev'])
elapsed = time.time() - start
total += elapsed
print('    Seconds: {:.2f}'.format(elapsed))
print('    Deletes per second: {:.1f}'.format(count / elapsed))

print('Total seconds: {:.2f}'.format(total))
print('Total ops per second: {:.1f}'.format((count * 3) / total))
print('')