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
parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.sys.path.insert(0,parentdir) 

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.split(os.path.dirname(__file__))[0])
       
from freestation.logger import Logger
LOG = Logger('GUI').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk, Gtk #@UnresolvedImport
from gi.repository import GdkX11 #@UnresolvedImport # For get_xid() @UnusedImport
from gi.repository import GObject #@UnresolvedImport

GObject.threads_init()

from freestation.constants import APP_NAME 
from freestation.widget_loader import WidgetLoader

from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

class GUI(Gtk.Window):
    __gtype_name__ = 'GUI'
    __name__ = 'GUI' #@ReservedAssignment
    
    DEFAULT_BACKGROUND   = '#660707'
    DEFAULT_BORDER_WIDTH = 24
    
    DEFAULT_WIDTH  = 960 # Default Gtk.Window width
    DEFAULT_HEIGHT = 840 # Default Gtk.Window height
    
    uclm_demo_couch = True
    
    def __init__(self, application):
        Gtk.Window.__init__(self, type = Gtk.WindowType.TOPLEVEL)

        self.set_default_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        self.set_size_request(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        
        LOG.debug('Starting')
        
        from freestation.constants import APP_ICON
        self.set_icon_from_file(join(file_path, 'img', APP_ICON))
        
        # http://faq.pygtk.org/index.py?file=faq03.002.htp&req=show
        self.add_events(
                          Gdk.EventMask.KEY_PRESS_MASK |
                          Gdk.EventMask.POINTER_MOTION_MASK |
                          Gdk.EventMask.BUTTON_PRESS_MASK | 
                          Gdk.EventMask.SCROLL_MASK
                        )
        """
        def wakeup(widget, event):
            " "" (button 4 for scroll up, button 5 for scroll down). " ""
            print "Event number %d woke me up" % event.type
     
        self.connect('motion-notify-event', wakeup)
        self.connect('key-press-event',     wakeup)
        self.connect('button-press-event',  wakeup)
        self.connect('scroll-event',        wakeup)
        """
        
        #Gtk.Window.set_default_icon_name('freestation')
        
        settings = Gtk.Settings.get_default()
        #settings.set_property("gtk-error-bell", False)

        theme = settings.get_property('gtk-theme-name')
        
        LOG.debug('Theme: {0}'.format(theme))
        
        provider = Gtk.CssProvider()
        provider._theme_name = theme.lower()
        
        screen = Gdk.Screen.get_default()
        context = self.get_style_context()
        
        
        if hasattr(self, '_css_provider'):
            # check old provider, see if we can skip setting or remove old
            # style provider
            if self._css_provider._theme_name != theme.lower():
                # clean up old css provider if exixts
                context.remove_provider_for_screen(screen, self._css_provider)
        
        ###provider.load_from_path('/home/shakaran/Escritorio/software-center/data/ui/gtk3/css/softwarecenter.css')
        ###context.add_provider_for_screen(screen, provider, 800)
        
        #screen = self.get_screen()
        #screen.get_display().sync()
        #screen.get_display().close()
        
        
        self.application = application
        self.__connect_signals()
        
        self.set_title(APP_NAME)
        self.set_border_width(self.DEFAULT_BORDER_WIDTH)
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
        
        self.realize() # Realize the window for get xid

        self.__load_widgets()

        self.__pack_widgets()

        self.add(self.box)
        self.fullscreen()

        self.show_all()
        
        #self.videoarea.xid = self.videoarea.get_property('window').get_xid()
        #print 'XID', self.videoarea.xid
        #self.videoarea.player.set_window_handle(self.videoarea.xid)
        ###self.videoarea.play()
    
    def __load_widgets(self):
        ''' 
            Load widgets (components) 
        '''
        self.widgets = WidgetLoader().get_widgets()
        
        for (name, properties) in self.widgets:
            LOG.debug('Requested widget: ' + str(name))
            widget_error = False

            mod = __import__('freestation.widgets', fromlist = [str(name)])

            try:
                mod_class = getattr(mod, name)
            except AttributeError as e: #@UnusedVariable
                LOG.error('Error: could not load the widget ' + str(name))
                widget_error = True
              
            if not widget_error:  
                LOG.info('Loaded: ' + str(mod_class))
                
                klass = getattr(mod_class, name)
                LOG.debug(klass)
                
                LOG.debug('Properties: ' + str(properties))
                
                for (key, value) in properties:
                    if key == 'data':
                        data = value
                
                LOG.debug('Invoking ' + str(klass))
                if data:
                    try:
                        temporal_object = klass(data) #[TODO] Load from properties
                    except TypeError as e:
                        temporal_object = klass()
                else:
                    temporal_object = klass()
                   
                if hasattr(temporal_object, 'set_properties'):
                    temporal_object.set_properties(properties)
                
                if hasattr(temporal_object, 'start'):
                    temporal_object.start()
                    
                temporal_attribute = temporal_object.__class__.__name__
                   
                # Create lowercase with underscore attribute class from name widget
                name_attribute = ''
                i = 0
                for letter in temporal_attribute:
                    if letter.isupper():
                        if i == 0:
                            letter = letter.lower()
                        else:
                            letter = '_' + letter.lower()
                        
                    name_attribute += str(letter)
                    i += 1
                   
                # Create attribute on class with metadinamic class created
                setattr(self, name_attribute + '_widget', temporal_object)
        
        """
        #screen = self.get_window().get_screen()
        for x in dir(Gdk.get_default_root_window().get_screen()):
            print x
        screen = Gdk.get_default_root_window().get_screen()
        print 'N monitors', screen.get_n_monitors()
        print 'Primary monitor', screen.get_primary_monitor
        print screen.get_display().get_name()
        print screen.get_display().get_n_screens()
        print screen.get_display().close()
        """
    
    def __pack_widgets(self):
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 0)
        self.box.set_border_width(0)
            
        self.main_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        self.middle_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
        self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        
        ##if hasattr(self, 'logo_area_widget'):
        ##    self.main_box.pack_start(self.logo_area_widget, expand = False, fill = False, padding = 0)
            
        ##if hasattr(self, 'title_display_widget'):
        ##    self.main_box.pack_start(self.title_display_widget, expand = False, fill = False, padding = 0)

        #self.hbox.pack_start(self.main_box, expand = False, fill = False, padding = 0)
        
        
        # Not work, needs pygst (GStreamer with GTK 3.0), because conflict gobject with GObject
        #box.pack_start(video_area, False, True, False) 
        
        
        #if hasattr(self, 'browser_view_widget'):
            # self.hbox.pack_start(self.browser_view_widget , True, True, True)
            
        """if hasattr(self, 'mount_info_widget'):
            self.progress_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 6)
            self.progress_box.pack_start(Gtk.Label(), True, True, False)

            self.progress_box.pack_start(child = self.mount_info_widget, expand = False, fill = False, padding = 0)
            
            self.progress_box.pack_start(Gtk.Label(), True, True, False)
        
            ##self.vbox.pack_start(child = self.progress_box, expand = False, fill = False, padding = 0)
        """
        
        ###self.box.pack_start(self.hbox, expand = False, fill = False, padding = 0)
        ###self.box.pack_start(self.vbox , True, True, True)
        
        
        #from freestation.widgets.FeedReader import FeedReader #@UnresolvedImport
                
        #feed_reader = FeedReader()
        
        ###self.middle_box.pack_start(feed_reader, expand = False, fill = False, padding = 0)
        
        
        #if hasattr(self, 'video_area_widget'):
            
        from freestation.widgets.VideoArea import VideoArea
        
        #fixed = Gtk.Fixed()
        #fixed.show()
        
        import os

        video = 'freestation/ogv/orbit.ogv'
        
        #self.videoarea = VideoArea(video)
        #self.videoarea.create_player()
        ##self.videoarea.load_player()
        ##self.videoarea.show()
        
        #g_upimage.set_margin_left(5)
        #g_upimage.set_margin_top(5)
        #g_upimage.set_margin_bottom(5)
        #g_upimage.set_margin_right(5)
        
        #label.set_margin_left(10)
        
        #g_sep = Gtk.HSeparator()
        #g_box.pack_start(g_sep, True, False, 0)
                
                
                
        ##self.middle_box.pack_start(self.videoarea, True, True, True)
        
        #self.box.pack_start(self.middle_box, True, True, True)


        
        ###from freestation.widgets import HtmlRenderer #@UnresolvedImport
        
        ###html_renderer = HtmlRenderer.HtmlRenderer()
        
        #self.box.pack_start( html_renderer, True, True, True)
        
        from freestation.widgets.ButtonSection import ButtonSection

        def icon_load(icon_name):
            icon = os.path.split(os.path.dirname(__file__))[0] + "/img/" + icon_name
            return icon
        
        
        if self.uclm_demo_couch:
            from freestation.widgets.UclmDemoCouch import UclmDemoCouch
            self.uclm_demo = UclmDemoCouch()
            
            self.set_border_width(0)
            self.box.pack_start(self.uclm_demo, True, True, True)
            
            GObject.idle_add(self.uclm_demo.on_idle)
        else:
            from freestation.widgets.UclmDemo import UclmDemo
            self.uclm_demo = UclmDemo()
    
            self.uclm_demo.main_page()
            
            self.box.pack_start(self.uclm_demo, True, True, True)
            
            

        """
        icon = icon_load('icon-teacher.png')
        
        first_row = Gtk.HBox()
        first_row.pack_start(ButtonSection('Magisterio', icon, 'pink'), True, True, True)
        first_row.pack_start(ButtonSection('Derecho', icon, 'blue'), True, True, True)
        first_row.pack_start(ButtonSection('Empresariales', icon, 'green'), True, True, True)
        
        second_row = Gtk.HBox()
        second_row.pack_start(ButtonSection('Medicina', icon, 'yellow'), True, True, True)
        second_row.pack_start(ButtonSection('Química', icon, 'orange'), True, True, True)
        second_row.pack_start(ButtonSection('Informática', icon, 'violet'), True, True, True)
        
        button_box = Gtk.VBox()
        button_box.pack_start(first_row, True, True, True)
        button_box.pack_start(second_row, True, True, True)
        """
        
        #self.box.pack_start(button_box, True, True, True)
        
        
        ###if hasattr(self, 'menu_actions_area_widget'):
        ###    self.box.pack_start(self.menu_actions_area_widget, expand = False, fill = False, padding = 0)
    
    def __connect_signals(self):
        self.connect('key-press-event', self.__key_press_event)
        self.connect('delete-event',   self.application.on_destroy)
               
    def __key_press_event(self, widget, event) :
        # event.keyval == Gdk.keyval_from_name("w")

        if event.string == 'q' :
            if hasattr(self, 'browser_view_widget'):
                self.browser_view_widget.on_destroy()
            widget.destroy()
            self.application.on_destroy(widget, event) 
        elif event.string == 'f' :
            self.unfullscreen()
        
        