#!/usr/bin/env python
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

import time

class Timer(object):
    def __init__(self):
        self.__start = time.time()

    def duration_in_seconds(self):
        self.__finish = time.time()
        
        return self.__finish - self.__start