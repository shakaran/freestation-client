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

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from gi.repository import Pango #@UnresolvedImport
from gi.repository import GdkPixbuf #@UnresolvedImport
from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

class ButtonSection(Gtk.VBox):
    
    DEFAULT_BACKGROUND   = '#660707'
    
    def __init__(self, text, image, background, boxed = True):
        Gtk.VBox.__init__(self, False)
        
        """try:
             self.icon = GdkPixbuf.Pixbuf.new_from_file(join('img', self.RSS_ICON))
        except:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(join(file_path, 'img', self.RSS_ICON))
        """
        self.icon = GdkPixbuf.Pixbuf.new_from_file(image)
        self.icon = self.icon.scale_simple(288, 90, GdkPixbuf.InterpType.BILINEAR)
        
        self.image = Gtk.Image()
        ##self.image.set_from_file(image)
        self.image.set_from_pixbuf(self.icon)
        self.image.set_alignment(0.0, 0.0)
        self.image.set_padding(5, 5)
        self.image.show()
        
        self.button = Gtk.Button(use_underline = False)
        self.button.set_use_underline(False)
        self.button.set_support_multidevice(True)
        self.button.set_sensitive(True)
        #self.button.set_border_width(50)
        self.button.set_alignment(0.5, 0)
        self.button.add(self.image)
        
        self.eb = Gtk.EventBox()
        self.eb.set_can_focus(True)
        self.eb.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(background))
        self.eb.set_halign(0.5)
        
        #print self.eb.get_default_style()

        font_color = "#ffffff"
        
        self.eb.modify_text(Gtk.StateType.NORMAL, Gdk.color_parse(font_color))
        self.eb.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('blue'))
        self.eb.set_tooltip_text(text)
        self.eb.modify_font(Pango.FontDescription('Mono'))
        self.eb.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
        
        self.eb.add(self.button)

        self.button_box = Gtk.HBox(False)
        
        if boxed:
            self.button_box.pack_start(Gtk.HBox(), True, True, True)
            
        self.button_box.pack_start(self.eb, False, False, False)
        
        if boxed:
            self.button_box.pack_start(Gtk.HBox(), True, True, True)
        
        self.label = Gtk.Label()
        self.label.set_selectable(False)
        self.label.set_margin_top(15)
        self.label.modify_text(Gtk.StateType.NORMAL, Gdk.color_parse(font_color))
        
        self.label.set_markup('<span color="{0}">{1}</span>'.format(font_color, text))
        
        
        self.pack_start(self.button_box, False, False, False)
        if boxed:
            self.pack_start(self.label, expand = False, fill = False, padding = 0)
        
        boxie = Gtk.EventBox()
        boxie.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.DEFAULT_BACKGROUND))
        
        self.add(boxie)
        
        """
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        """
        
        
        # Uncomment this for see space
        """
        self.boxie = Gtk.EventBox()
        self.boxie.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("red")) 
        
        self.add(self.boxie)
        """