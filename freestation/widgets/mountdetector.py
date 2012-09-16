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

# Initialize the gobject/dbus support for threading
from gi.repository import GObject #@UnresolvedImport @UnusedImport
#GObject.threads_init()

#import gobject
#gobject.threads_init() #@UndefinedVariable

import dbus #@UnusedImport
from dbus.mainloop.glib import DBusGMainLoop

import dbus.service
import traceback
import sys

import os
from urllib.parse import unquote
import logging
logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", None)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG = logging.getLogger('MountDetector')


class MountDetector:
    """
    Detect mount events from dbus session.
    
    Example of event fired on dbus:
    
    signal sender=:1.37 -> dest=(null destination) serial=131 path=/org/gtk/Private/RemoteVolumeMonitor; interface=org.gtk.Private.RemoteVolumeMonitor; member=MountRemoved
    string "org.gtk.Private.GduVolumeMonitor"
    string "0x9f7d940"
    struct {
       string "0x9f7d940"
       string "My Passport"
       string ". GThemedIcon drive-harddisk-usb drive-harddisk drive"
       string ""
       string "file:///media/My%20Passport"
       boolean true
       string ""
       array [
       ]
    }
    """
    
    disk_name = None
    
    MOUNT_SERVICE = 'org.gtk.Private.RemoteVolumeMonitor'
    
    def __init__(self, mount_info):
        """
        Create a dbus based monitor
        """
        self.mount_info = None
        
        if mount_info:
            self.mount_info = mount_info
        
            self.progress_bar_text = self.mount_info.get_children()[0]
            self.progress_bar      = self.mount_info.get_children()[1]
        
        self._create_session_bus()
        self._check_service()
        self._connect_signals()

        #loop = GObject.MainLoop() 
        #loop.run()
   
    def _create_session_bus(self):
        LOG.info('DBus Version ' + '.'.join(map(str, dbus.version)))
        
        # Setting the DBusGMainLoop as default which allows to receive DBus 
        # calls during the gtk.main loop
        dbus_loop = DBusGMainLoop(set_as_default = True)
        
        self._session_bus = dbus.SessionBus(mainloop = dbus_loop)
        #print 'Dbus services:', str(self._session_bus.list_names())
   
    def _connect_signals(self):
        """
        This code could be replaced by gio.VolumeMonitor that is actually a high
        level abstraction for dbus mount signals. But for the purpose of the
        application use only a couple of calls of dbus is more useful.
        
        from gio import VolumeMonitor
        self._volume_monitor = VolumeMonitor()
        self._volume_monitor.connect('mount-added', self._add_mount)
        self._volume_monitor.connect('mount-removed', self._remove_mount)
        """
        
        # connect dbus signals
        self._session_bus.add_signal_receiver(
                                              self._mount_added,
                                              'MountAdded',
                                              self.MOUNT_SERVICE
                                              )
        self._session_bus.add_signal_receiver(
                                             self._mount_removed,
                                             'MountRemoved',
                                             self.MOUNT_SERVICE
                                            )
   
    def _check_service(self):
        try: 
            service = dbus.service.BusName(self.MOUNT_SERVICE, self._session_bus) 
            
            #print service.get_bus()
            LOG.info('Service name: %s' % (service.get_name()))
        except dbus.DBusException as e: 
            sys.stderr.write('Error: MountDetector on dbus session: %s\n' % str(e))
            LOG.exception(traceback.print_exc()) 
            sys.exit(1) 
        
        
    def _mount_added(self, sender, mount_id, data):
        """
        Handle adding of new device
        
        Using gio.VolumeMonitor result as:
        
        def _add_mount(self, monitor, mount):
            icon_names = mount.get_icon().to_string()
            print icon_names
            print mount.get_name()
            print mount.get_root()
            print mount.get_root().get_path()
            print mount
            print monitor
        """

        # Another parse way: data[4].split('://')[1]
        disk_name = unquote(data[4][7:]) # Remove chars like %20 or similar
        print (disk_name)
        
        self.disk_name = disk_name
        
        disk = os.statvfs(disk_name)
        
        print ("preferred block size", "=>", disk.f_bsize)
        print ("fundamental block size", "=>", disk.f_frsize)
        print ("total blocks", "=>", disk.f_blocks)
        print ("total free blocks", "=>", disk.f_bfree)
        print ("available blocks", "=>", disk.f_bavail)
        print ("total file nodes", "=>", disk.f_files)
        print ("total free nodes", "=>", disk.f_ffree)
        print ("available nodes", "=>", disk.f_favail)
        print ("max file name length", "=>", disk.f_namemax)
        
        totalSize = (disk.f_bsize * disk.f_bfree)
        print (totalSize) # Size MB
        print (self.convert_bytes(totalSize))
        
        capacity = disk.f_bsize * disk.f_blocks
        print (self.convert_bytes(capacity))
        
        # Available bytes = Prefererred block zize * Available blocks
        available = disk.f_bsize * disk.f_bavail
        print (self.convert_bytes(available))
        
        print ('totalsize', totalSize)
        print ('capacity', capacity)
        print ('available', available)
        
        # Used bytes = Prefererred block zize * (Total blocks - Available blocks)
        # used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
        # print self.convert_bytes(used)
        
        #label = data[1]
        #icon = self._application.icon_manager.get_mount_icon_name(data[2])
        #mount_point = data[4].split('://')[1]

        #self._add_item(label, mount_point, mount_id, icon)
        
        # Storage: My Passort 16GB/450 GB available
        if self.mount_info:
            self.progress_bar_text.set_label('Storage: ' + os.path.basename(disk_name) + '    ' + self.convert_bytes(totalSize) + '/' + self.convert_bytes(capacity) + ' available')
            self.progress_bar.set_fraction(totalSize / float(capacity))
            self.progress_bar.set_text(self.convert_bytes(totalSize) + '/' + self.convert_bytes(capacity))
            
        self.on_mount_added(os.path.basename(disk_name), self.convert_bytes(totalSize), self.convert_bytes(capacity), ((capacity - totalSize ) / float(capacity)) * 100)
     
    def on_mount_added(self, disk_name, total_size, capacity, percent):
        pass

    def _mount_removed(self, sender, mount_id, data):
        """Handle removal of device"""
        
        print ('mount removed')
        
        if self.mount_info:
            self.progress_bar_text.set_label('Storage: device no detected')
            self.progress_bar.set_fraction(0)
            self.progress_bar.set_text('-')
        
        print (data)
        
        self.on_mount_removed(sender, mount_id, data)
        #mount_point = data[4].split('://')[1]
        #self._remove_item(mount_point)

    def on_mount_removed(self, sender, mount_id, data):
        pass
    
    def convert_bytes(self, bytes): #@ReservedAssignment
        '''
        
        @param bytes:
        '''
        bytes = float(bytes) #@ReservedAssignment
        if bytes >= 1099511627776:
            terabytes = bytes / 1099511627776
            size = '%.2f TiB' % terabytes
        elif bytes >= 1073741824:
            gigabytes = bytes / 1073741824
            size = '%.2f GiB' % gigabytes
        elif bytes >= 1048576:
            megabytes = bytes / 1048576
            size = '%.2f MiB' % megabytes
        elif bytes >= 1024:
            kilobytes = bytes / 1024
            size = '%.2f KiB' % kilobytes
        else:
            size = '%.2f B' % bytes
        return size

#MountDetector()