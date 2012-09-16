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

from freestation.logger import Logger
LOG = Logger('UclmDemoCouch').get()

import sys
from os import path
import os
import microfiber #@UnresolvedImport
import dbus
from dbus.mainloop.glib import DBusGMainLoop

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GObject #@UnresolvedImport

from freestation.widgets.Hub import hub_factory
from freestation.widgets.dataprovider import DataProvider
from freestation.widgets.Browser import Browser

file_path = str(os.path.split(os.path.dirname(__file__))[0])
APPS = '/usr/share/couchdb/apps/'

GObject.threads_init()
DBusGMainLoop(set_as_default=True)

import json
def handler(d):
    assert path.abspath(d) == d
    print ('Handler', d)
    return     '{{couch_httpd_misc_handlers, handle_utils_dir_req, {}}}'.format(
        json.dumps(d)
    )

class UclmDemoCouch(Gtk.VPaned):
    name = 'freestation'  # The namespace of your app, likely source package name
    dbname = 'freestation-0'  # Main CouchDB database name
    
    PAGE = 'uclm_demo.html'
    
    proxy_bus = 'org.freedesktop.DC3'  # Dbus service that will start CouchDB
    proxy_path = '/'
    
    signals = {
        'loaded': ['time'],
        'on_load': ['data'],
        'on_fs_request': ['data', 'side'],
        'updater': ['data', 'side'],
        'updater_description': ['data'],
        'on_get_description': ['data'], # method
        'mount_added': ['name', 'total_size', 'capacity', 'percent'], # signal send to html
        'copyusb': ['usb_data'], # signal gtk recieved send via html
        'copyusb_finished' : [],
    }
    
    enable_inspector = True
            
    def __init__(self):
        Gtk.VPaned.__init__(self)

        self.env = None
        self.inspector = None
        self.set_border_width(0)

        # Figure out if we're running in-tree or not        
        script = path.abspath(sys.argv[0])
        print ('stript:{0}'.format(script))
        tree = path.dirname(script)
        print ('tree:{0}'.format(script))
        ui = path.join(tree, 'ui')
        self.intree = True
        self.ui = (ui if self.intree else path.join(APPS, self.name))
        print ('ui:{0}'.format(self.ui))
        
        self.view = Browser()
        self.view.connect('render-finished', self.on_render_finished)

        self.view.settings.set_property('enable-developer-extras', True)
        if self.enable_inspector:
             # Enable webkit inspector
            inspector = self.view.get_inspector()
            inspector.connect('inspect-web-view', self.on_inspect)

        vbox = Gtk.VBox(False, 0)
        vbox.pack_start(self.view, True, True, 0)
        
        #self.pack1(self.scroll, True, True)
        self.pack1(vbox, True, True)
        
    def connect_hub_signals(self, hub):
        hub.connect('loaded', self.on_loaded)
        hub.connect('on_fs_request', self.on_fs_request)
        hub.connect('on_get_description', self.on_get_description)
        hub.connect('copyusb', self.on_copyusb)
        
    def on_copyusb(self, hub, usb_data = None):
        print ('Copying usb data')
        print (usb_data)
        
        disk_name = self.mount_detector.disk_name
        
        if disk_name:
            import shutil
            
            usb_folder = str(disk_name) + '/freestation/'
            
            if not os.path.exists(usb_folder):
                os.makedirs(usb_folder)
            
            for file in usb_data:
                print (file_path)
                print('Copying ' + str(file) + '.png')
                shutil.copy2(file_path + '/files/' + str(file) + '.png', str(usb_folder) + str(file) + '.png')
            
            import time
            time.sleep(2)
        
        hub.send('copyusb_finished')
        
        
    def load(self, url = 'http://www.uclm.es'):
        print ('load page:{0}'.format(url))
        path = '/_intree/' + url
        print ('path:{0}'.format(path))
        full_url = self.server._full_url(path)
        print ('full_url:{0}'.format(full_url))
        self.view.load_uri(full_url)

    
    def on_render_finished(self, view):
        print ('Render finished on UclmDemoCouch')
        #print view # Browser
         
    def on_destroy(self):
        print ('On destroy UclmDemoCouch')
        
        if self.view.inspector:
            self.view.inspector.destroy()
        
    def on_idle(self):
        session = dbus.SessionBus()
        self.proxy = session.get_object(self.proxy_bus, self.proxy_path)
        
        if self.proxy:
            env = json.loads(self.proxy.GetEnv())
            print ('env:{0}'.format(env))
        else:
            print ('No proxy found')

        self.view.show()
        
        print ('Creating hub')
        # Create the hub
        self.hub = hub_factory(self.signals)(self.view)
        print ('Connecting hub signals')
        self.connect_hub_signals(self.hub)
        
        from freestation.widgets.mountdetector import MountDetector
        
        class CustomMountDetector(MountDetector):
        
            def __init__(self, hub):
                super().__init__(None)
                self.__hub = hub
                
            def on_mount_added(self, disk_name, total_size, capacity, percent):
                print (disk_name +  total_size + capacity + str(percent))
                self.__hub.send('mount_added', disk_name, total_size, capacity, str(percent))
        
        self.mount_detector = CustomMountDetector(self.hub)
        
        print ('Set enviroment')
        self.set_env(env)
        self.load(self.PAGE)
    
    def set_env(self, env):    
        self.env = env
        print ('creating server')
        self.server = microfiber.Server(env)
        print ('creating db')
        #self.db = microfiber.Database(self.dbname, env) 
        #self.db.ensure()
        if self.intree:
            self.server.put(
                handler(self.ui), '_config', 'httpd_global_handlers', '_intree'
            )
        self.view.set_env(env)
        if self.inspector is not None:
            self.inspector.view.set_env(env)
    
    def on_loaded(self, hub, data):
        print ('On loaded!' + str(hub) + str(data))
        #hub.send('on_load', 'load received')
        
    def on_get_description(self, hub, data):
        print ('on_get_description data:'  + (data))
        
        self.data_provider = DataProvider()
        
        result = self.data_provider.data['description']['distribution']['default']
        
        try:
            result = self.data_provider.data['description']['distribution'][data]
        except Exception:
            result = self.data_provider.data['description']['distribution']['default']

        hub.send('updater_description', result)
        
    def on_fs_request(self, hub, data, side = 'left'):
        print ('on_fs_request data:'  + (data) + ' side:' + side)

        self.data_provider = DataProvider()

        try:
            result = self.data_provider.data['panel'][data]
        except Exception:
            result = 'default data'
            
        hub.send('updater', result, side)
        
    def on_inspect(self, inspector, view):
        from freestation.widgets.inspector import Inspector
        
        self.inspector = Inspector(None, self)

        view.get_parent().get_parent().pack2(self.inspector, True, True)

        self.inspector.show_all()
        self.inspector.reload.connect('clicked', self.on_reload)
        self.inspector.futon.connect('clicked', self.on_futon)
        return self.inspector.view

    def on_reload(self, button):
        self.view.reload_bypass_cache()

    def on_futon(self, button):
        full_url = self.server._full_url('/_utils/')
        print ('full_url:{0}'.format(full_url))
        self.view.load_uri(full_url)            