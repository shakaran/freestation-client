#!/usr/bin/env python2.7
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 
#
# This file is part of FreeStation.
#
# FreeStation is free software; you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
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

import sys
import traceback
import Ice #@UnresolvedImport

# Load FS module from fs.ice file
Ice.loadSlice('ice/fs.ice', ['-I' '/usr/share/slice'])
import FS #@UnresolvedImport

import IceBox #@UnusedImport @UnresolvedImport
 
from timer import Timer #@UnresolvedImport

class FreeStationClient(Ice.Application):

    SERVER_IP = '123.123.123.123' # Put here your server IP
    COMUNNICATOR_NAME = 'Api'
    PORT = 10000 
    VERSION = '0.1'
    MODE = 'udp' # connection mode: tcp or udp
    TIMEOUT = 60000 # 60 secs
    DEFAULT_CHUNK_FILE_SIZE = 1024 * 150 # 150 KB
    
    def __init__(self):
        print ('FreeStation Client ' + str(self.VERSION))
        
        self.__loadIceInterface()
        
    def __loadIceInterface(self):
        ice_version = Ice.stringVersion()
        print ('Ice Version ' + str(ice_version))

    def create_base(self):
        self.base = None
        
        try:
            self.base = self.communicator().stringToProxy('Api:default -h ' + str(self.SERVER_IP) + ' -t ' + str(self.TIMEOUT) + ' -p ' + str(self.PORT) + ':' + self.MODE + ' -z')
        except Ice.EndpointParseException as e: #@UndefinedVariable
            sys.stderr.write('Error: could not create end point: %s\nClient abort.\n' % str(e.str))
            return -1
        
        # Print remote object reference
        print ('Base: ' + str(self.base))
        
    def create_proxy(self):
        try:
            self.proxy = FS.ApiPrx.checkedCast(self.base) #@UndefinedVariable
        except Ice.ConnectionRefusedException as e: #@UndefinedVariable
            if e.error == 111:
                sys.stderr.write('Error: connection refused. Please, check if the server is running or you are connecting properly.\nClient abort.\n')
            else:
                sys.stderr.write('Error: %s\nClient abort.\n' % str(e))
                #print e.ice_name()
                #print e.message
                #print e.error
            return -1
        except Ice.NoEndpointException as e: #@UndefinedVariable
            sys.stderr.write('Error: could not find end point\n%s\nClient abort.\n' % str(e.proxy))

            return -1
        except Ice.UnknownLocalException as e: #@UndefinedVariable
            sys.stderr.write('Error: unknown local exception %s\nClient abort.\n' % str(dir(e)))

            return -1
        except Ice.MarshalException as e: #@UndefinedVariable
            sys.stderr.write('Error: could not marshal call: %s\nClient abort.\n' % str(dir(e)))

            return -1
        except Exception as e:
            sys.stderr.write('Error: unknow exception: %s\nClient abort.\n' % str(dir(e)))

            return -1
        
        if not self.proxy:
            sys.stderr.write('Error: could not create proxy.\nClient abort.\n')
            return -1

        print ('Proxy: ' + str(self.proxy))
    
    def is_authorized(self):
        try:
            return self.proxy.isAuthorized()
        except Ice.OperationNotExistException as e: #@UndefinedVariable
            # http://doc.zeroc.com/display/Ice/Ice-OperationNotExistException
            sys.stderr.write('Error: operation does not exist: %s\nMaybe you are using a outdated Slice specification.\nClient abort.\n' % str(e.operation))
            
            return 0
        except Ice.ConnectionLostException as e: #@UndefinedVariable
            sys.stderr.write('Error: The connection to server was lost: %s\nClient abort.\n' % str(e.__str__()))
            
            return 0
        
        except Exception as e:
            sys.stderr.write('Error: could not get FS server version %s\nClient abort.\n' % str(e))
            #print 'Message:' + e.message
            #print 'Error:' + str(e.unknown)
            #print 'ice_name:' + str(e.ice_name())
            #print 'String:' + e.__str__()
            
            return 0
        
    def get_server_version(self):
        print ('FS Server version:')
        try:
            print (self.proxy.version())
        except Ice.OperationNotExistException as e: #@UndefinedVariable
            # http://doc.zeroc.com/display/Ice/Ice-OperationNotExistException
            sys.stderr.write('Error: operation does not exist: %s\nMaybe you are using a outdated Slice specification.\nClient abort.\n' % str(e.operation))
            
            return -1
        except Ice.UnknownException as e: #@UndefinedVariable
            if e.unknown.find('NoAuthorized: ') != -1:
                sys.stderr.write('This FreeStation client is no authorized by the server\nClient abort.\n')
            if e.unknown.find('ClientStatusDisabled: ') != -1:
                sys.stderr.write('This FreeStation client is authorized but disabled by the server\nClient abort.\n')
            else:
                sys.stderr.write('Error: unknown exception trying to get FS server version %s\nClient abort.\n' % str(e))
            
            return -1
        except Ice.ConnectionLostException as e: #@UndefinedVariable
            sys.stderr.write('Error: The connection to server was lost: %s\nClient abort.\n' % str(e.__str__()))
            
            return -1
        
        except Exception as e:
            sys.stderr.write('Error: could not get FS server version %s\nClient abort.\n' % str(e))
            #print 'Message:' + e.message
            #print 'Error:' + str(e.unknown)
            #print 'ice_name:' + str(e.ice_name())
            #print 'String:' + e.__str__()
            
            return -1
        
    def request_file(self, file_requested = None):

            file_size = self.proxy.getFileSize(file_requested)
            print ('File size: ' + str(file_size) + ' Bytes')
            
            file_download = open(file_requested, 'w')
            
            timer = Timer()
            
            # 1.5 MB = 137 sec (1 KB)
            # 1.5 MB = 16 sec (10 KB)
            # 1.5 MB = 4 sec (50 KB)
            # 1.5 MB = 2.84 sec (100 KB)
            # 1.5 MB = 2.67 sec (150 KB)
            # 1.5 MB = 2.26 sec (500 KB)
            # 700 MB = 961 sec (16 min) (150 kb) 747 KB/s
            
            for size in range(0, file_size, self.DEFAULT_CHUNK_FILE_SIZE): # Loop each chunk size KB
                #print 'Requesting size: ' + str(size)
                async_result = self.proxy.begin_getFileChunk(file_requested, size, self.DEFAULT_CHUNK_FILE_SIZE) # Chunks
                #print 'Async call processed (' + str(size) + ')'
        
                try:
                    data = self.proxy.end_getFileChunk(async_result) # Ice::MemoryLimitException or timeout
                except Ice.CommunicatorDestroyedException as e: #@UndefinedVariable ::Ice::CommunicatorDestroyedException
                    sys.stderr.write('Error: The connection to comunicator was destroyed.\nClient abort.\n')
                    return -1
                
                except Exception as e:
                    sys.stderr.write('Error: unknown exception in request_file %s\nClient abort.\n' % str(e))
                    #print 'Message:' + e.message
                    #print 'Error:' + str(e.unknown)
                    #print 'ice_name:' + str(e.ice_name())
                    #print 'String:' + e.__str__()
                    
                    return -1
        
                speed = size / timer.duration_in_seconds()
                
                if size / 1024.0 < 1024:
                    size = str(round(size / 1024.0, 2)) + ' KB'
                elif size / (1024.0 * 1024.0) < 1024:
                    size = str(round(size / (1024.0 * 1024.0), 2)) + ' MB'
                elif size / float(1024.0 * 1024.0 * 1024.0) < 1024:
                    size = str(round(size / (1024.0 * 1024.0 * 1024.0), 2)) + ' GB'  
                
                file_download.write(data)
                
                if speed / 1024.0 < 1024:
                    speed = str(round(speed / 1024.0, 2)) + ' KB/s'
                elif speed / (1024.0 * 1024.0) < 1024:
                    speed = str(round(speed / (1024.0 * 1024.0), 2)) + ' MB/s'
                elif speed / (1024.0 * 1024.0 * 1024.0) < 1024:
                    speed = str(round(speed / (1024.0 * 1024.0 * 1024.0), 2)) + ' GB/s'   
                    
                print ('Received (' + str(size) + ') ' + 'Speed: ' + str(speed))  
                
            file_download.close()
            
            print ('Data saved in ' + str(timer.duration_in_seconds()) + ' seconds')
        
    def run (self, argv):
        '''
        @param argv: arguments
        @type argv: list
        '''

        if self.create_base() == -1:
            return -1
        
        if self.create_proxy() == -1:
            return -1
    
        #if self.get_server_version() == -1:
        #    return -1

        print ('Checking if client autorized')
        
        if not self.is_authorized():
            sys.stderr.write('Error: client no authorized or disabled\nClient abort.\n')
            return 1
        else:
            print ('Client authorized.')

            print ('Client ID: ' + str(self.proxy.getClientId()))
            
            """
            Example for enable widget download:
            print ('Requesting widgets.xml configuration ...')
            
            widgets_xml_config = str(self.proxy.getXMLWidgets())
            
            print (widgets_xml_config)
            
            print ('Configuration saved.')
            widgets_file = open('xml/widgets.xml', 'w')
            widgets_file.write(widgets_xml_config)
            widgets_file.close()
            """
            
            """Example for enable file download:"""
            print ('Downloading files for client ...')
            print ('Requesting test.tar.gz file ...')
            if self.request_file('test.tar.gz') == -1:
                return -1
            
            #self.request_file('ubuntu-12.04.iso')
            """
            print ('Ping test')
            print (self.proxy.ice_ping())
            print (self.proxy.ice_id())
            print (self.proxy.ice_ids())
            #print proxy.getInfo()
            """
            
            print ('Exit')
        
        return 0
 
 
config_file = None

data = Ice.InitializationData()
data.properties = Ice.createProperties(None, data.properties)
data.properties.setProperty('Ice.Config', '0')
data.properties.setProperty('Ice.ProgramName', 'FreeStationClient')
data.properties.setProperty('Ice.MessageSizeMax', '1024000') # 10240 KB = 10 MB (default 1 MB) 

#data.properties.setProperty('Ice.Default.Protocol', 'udp')
data.properties.setProperty('Ice.Override.Compress', '1')
data.properties.setProperty('Ice.ACM.Client', '60')


sys.exit(FreeStationClient().main(sys.argv, config_file, data))