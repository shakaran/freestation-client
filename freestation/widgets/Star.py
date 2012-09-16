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

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport

import cairo
# http://cairographics.org/documentation/pycairo/2/reference/context.html#cairo.Context.copy_page

class Star(Gtk.EventBox):
    def __init__(self):
        Gtk.EventBox.__init__(self)
        self.set_visible_window(False)
        
        self.connect('draw', self.on_draw)
        print 'Cairo' , cairo.cairo_version_string()

    
    def _create_surface(self, image_format = cairo.FORMAT_ARGB32, width = 50, height = 50):
        """
            Create a surface that render to memory buffers either allocated by cairo
            
            format: type of image default is:
                cairo.FORMAT_ARGB32: 32-bit image native-endian with alpha in the upper 8 bits, then red, then green
            width: the image width on pixels      
            height: the image height on pixels     
        """
        # Check if supported
        if cairo.HAS_IMAGE_SURFACE:
            self.image_surface = cairo.ImageSurface(image_format, width, height)
        else:
            raise RuntimeError('Image surface is not supported by Cairo. Please install the module.')   
    
    def on_render(self, widget_context, window_context):
        #widget_context
        
        rgba1 = widget_context.get_border_color(Gtk.StateFlags.NORMAL)
        rgba0 = widget_context.get_color(Gtk.StateFlags.ACTIVE)

        #Set a Pattern to be used
        lin = cairo.LinearGradient(0, 0, 0, 50)
        lin.add_color_stop_rgb(0, rgba0.red, rgba0.green, rgba0.blue)
        lin.add_color_stop_rgb(1, rgba1.red, rgba1.green, rgba1.blue)
        
        self._create_surface()
        
        # Create a context with the target surface
        try:
            context = cairo.Context(self.image_surface)
        except MemoryError:
            print 'Error: No enough memory for create a context'
            
        context.set_source(lin)
        context.close_path()
        
        image_surface_width = self.image_surface.get_width()
        print 'surface with', image_surface_width
        
        del context
        
        window_context.set_source_rgb(0.2, 0.23, 0.9)
        
        #window_context.rectangle(0, 0, image_surface_width, 20)
        #window_context.clip()
        window_context.set_source_surface(self.image_surface, 0, 0)
        window_context.fill()
        
        window_context.set_source_rgba(1, 0, 0, 0.80)
        window_context.fill()
        
        window_context.paint()
        
        #window_context.reset_clip()
        """
        if fraction < 1.0:
            empty_width = stars_width - full_width
            cr.rectangle(x+full_width, y, empty_width, star_height)
            cr.clip()
            cr.set_source_surface(empty, x, y)
            cr.paint()
            cr.reset_clip()
        """
        return
        
    
    def on_draw(self, widget, window_context):
        style_context = widget.get_style_context()
        self.on_render(style_context, window_context)
            
        # drawing options for the Context
if __name__ == '__main__':
    win = Gtk.Window()
    win.set_size_request(200, 200)

    vb = Gtk.VBox()
    vb.set_spacing(6)
    win.add(vb)
    
    vb.add(Gtk.Button())
    vb.add(Gtk.Label(label="BLAHHHHHH"))
    vb.add(Gtk.Button())
    
    star = Star()
    vb.pack_start(star, False, False, 0)
    
    vb.add(Gtk.Button())
    vb.add(Gtk.Label(label="BLAHHHHHH"))
    
    win.connect("destroy", Gtk.main_quit)
    
    win.show_all()
    Gtk.main()