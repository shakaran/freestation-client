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

from time import time, sleep
from os import getppid, getpid, kill, setpgrp, killpg
from signal import signal, SIGTERM, SIGKILL
import sys
from traceback import print_exc

from logger import Logger #@UnresolvedImport
LOG = Logger('Watchdog').get()

from freestationapp import FreeStationApp #@UnresolvedImport

class Watchdog(object):
    
    MONITOR_TIME = 1
    PROCESS_MONITORED_NAME = 'FreeStation'
    
    def __init__(self):
        ''' 
            Init the watchdog 
        '''
        
        LOG.debug('Parent PID: {0}'.format(getppid()))
        LOG.debug('Watchdog PID: {0}'.format(getpid()))
        
        signal(SIGTERM, self.handler)
        
        self.play = True
        
        self.threads = []
    
    def handler(self, signal, object): #@ReservedAssignment
        '''
            Catch SIGTERM signal and destroy the app if alive
        '''
        if hasattr(self, 'p'):
            if self.p and self.p.is_alive():
                self.p.on_destroy(None, None)
        
        LOG.debug('Exiting by interrupt. Bye')
        # This shows: Exception SystemExit: 0 in <module 'threading' from '/usr/lib/python2.7/threading.pyc'> ignored
        # But it is only closing with nice exit. SystemExit when it is not handled, the Python interpreter exits
        sys.exit(0) 
        
    def launch(self, alive_time = None, enable_gui = True):
        '''
            Launch the threaded application 
            @param alive_time msec for live app, normally used by test. Default None for ignore
            @param enable_gui launch the program loading the GUI if True
        '''
        if hasattr(self, 'p'):
            self.p.destroy()
            del self.p
            
        # Cleanup any state set by the FreeStationApp.
        #
        import signal #@Reimport
        #if signal.__dict__.has_key('SIGHUP'):
        #    signal.signal(signal.SIGHUP, signal.SIG_DFL)
        #if signal.__dict__.has_key('SIGBREAK'):
        #    signal.signal(signal.SIGBREAK, signal.SIG_DFL) #@UndefinedVariable
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        
        import os
        if os.path.exists('webkit.lock'):
            os.remove('webkit.lock')
        self.p = None
        self.p = FreeStationApp(alive_time, enable_gui)
        self.p.setName(self.PROCESS_MONITORED_NAME + '-' + str(time()))
        self.threads.append(self.p)
        self.p.start()

        
    def monitor(self, alive_time = None, enable_gui = True, executions = None):
        ''' 
            Check if the app is alive, and restart if the app dead 
        '''
        while(self.play):
            LOG.debug('Sleeping {0} seconds'.format(str(self.MONITOR_TIME)))
            sleep(self.MONITOR_TIME)
            
            if not hasattr(self, 'p'):
                self.launch(alive_time, enable_gui)
                
            LOG.debug('Checking if alive...')
            
            #print (self.threads)
            
            if(self.p.is_alive() == False):
                self.p.on_destroy(None, None)
                
                # Join all threads using a timeout so it doesn't block
                # Filter out threads which have been joined or are None
                self.threads = [t.join(1) for t in self.threads if t is not None and t.isAlive()]
            
                LOG.error('Restarting process ...')
                self.launch(alive_time, enable_gui)
                
                if executions:
                    executions -= 1
                    if executions <= 0:
                        self.exit()
            else:
                LOG.debug('Process still running: {0}'.format(self.p.getName()))

                self.p.join(timeout=1.0)
    
    def stop(self):
        self.play = False
    
    def exit(self): #@ReservedAssignment
        '''
            Send a SIGTERM himself
        '''
        kill(getpid(), SIGTERM)

if __name__ == '__main__':
    setpgrp() # create new process group, become its leader
    try:
        watchdog = Watchdog().monitor(None, True, None)
    except KeyboardInterrupt:
        LOG.debug('Exiting by keyboard. Bye')
        sys.exit(0)
    except Exception as e:
        sys.stderr.write('Fatal error: {0}\n'.format(str(e)))
        LOG.exception(print_exc()) 
        sys.exit(1) 
    finally: # Ensure kill all the children and avoid zombies
        LOG.debug('Ensure killing children zombie process')
        killpg(0, SIGKILL)