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
LOG = Logger('FeedReader').get()

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk #@UnresolvedImport
from gi.repository import Gdk #@UnresolvedImport
from gi.repository import GdkPixbuf #@UnresolvedImport

from os.path import join, split, dirname
file_path = str(split(dirname(__file__))[0])

from HTMLParser import HTMLParser
from freestation.widgets.NewsReader import NewsReader #@UnresolvedImport

class FeedReader(Gtk.Box):
    
    RSS_ICON = 'rss_logo.png'
    
    DEFAULT_BACKGROUND = '#ec8d12'
    
    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        LOG.debug('Starting')
        
        css = Gtk.CssProvider()
        print css.load_from_data("""
        GtkButton:active {
    background-color: #0274d9;
}

/* Theme buttons with the mouse pointer on it,
   both are equivalent */
GtkButton:hover,
GtkButton:prelight {
    background-color: #3085a9;
}

/* Theme insensitive widgets, both are equivalent */
:insensitive,
*:insensitive {
    background-color: #320a91;
}

/* Theme selection colors in entries */
GtkEntry:selected {
    background-color: #56f9a0;
}

/* Theme focused labels */
GtkLabel:focused {
    background-color: #b4940f;
}
GtkLabel:hover, GtkLabel:active, GtkLabel:selected {
    background-color: #b4940f;
}
        """)
        
        self.background = self.DEFAULT_BACKGROUND
        
        data = 'http://webpub.esi.uclm.es/actualidad/noticias.rss' 
        news_reader = NewsReader(data)
        news_reader.render()
        
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))
        
        
        Gdk.Cursor.new(Gdk.CursorType.HAND2)
        
        self.set_border_width(0)

        self.allocation = Gdk.Rectangle()
        
        title_label = Gtk.Label()
        title_label.set_justify(Gtk.Justification.CENTER)

        title_label.set_halign(Gtk.Align.END)
        title_label.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))

        bg='black'
        fg =  'blue'
        text = '<b>'  + news_reader.title + '</b>'

        self.pack_start(title_label, True, True, False)
        
        feed_label = Gtk.Label(news_reader.title)
        feed_label.set_justify(Gtk.Justification.LEFT) 
        feed_label.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))
        
        try:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(join('img', self.RSS_ICON))
        except:
            self.icon = GdkPixbuf.Pixbuf.new_from_file(join(file_path, 'img', self.RSS_ICON))
            
        self.icon = self.icon.scale_simple(32, 32, GdkPixbuf.InterpType.BILINEAR)
        
        self.rss_icon = Gtk.Image()
        self.rss_icon.set_from_pixbuf(self.icon)

        self.hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 0)
        self.hbox.pack_start(self.rss_icon, expand = False, fill = False, padding = 0)
        self.hbox.pack_start(feed_label, expand = False, fill = False, padding = 0)
        
        self.pack_start(self.hbox, expand = False, fill = False, padding = 0)
        
        content = news_reader.entries_result
        content = self.clean_html(content)
        
        feed_content = Gtk.Label(content)
        feed_content.set_size_request(100, 300)
        feed_content.set_width_chars(80) # This is the real with size
        feed_content.set_line_wrap(True)
        feed_content.set_justify(Gtk.Justification.LEFT) 
        feed_content.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(self.background))
        
        Gtk.rc_parse(join(file_path, 'themes', 'default.txt'))
        #Gtk.rc_parse_string("""style "default" {font_name = "sans 7"}""")
        Gtk.rc_reparse_all()

        style = feed_content.get_style()
        
        context = feed_content.get_style_context()
        context.add_class("backforward-left-button")

        self.pack_start(feed_content, expand = False, fill = False, padding = 0)
        
    def clean_html(self, html):
        """
        content = content.replace('<p>', '')
        content = content.replace('</p>', '')
        content = content.replace('<strong>', '')
        content = content.replace('</strong>', '')
        content = content.replace('&aacute;', 'á')
        content = content.replace('&eacute;', 'é')
        content = content.replace('&iacute;', 'í')
        content = content.replace('&oacute;', 'ó')
        content = content.replace('&uacute;', 'ú')
        content = content.replace('&nbsp;', ' ')
        """
        
        class MLStripper(HTMLParser):
            def __init__(self):
                self.reset()
                self.fed = []
            def handle_data(self, d):
                self.fed.append(d)
            def get_data(self):
                return ''.join(self.fed)
        
        def strip_tags(html):
            htmlparser = HTMLParser()
            html = htmlparser.unescape(html)
        
            s = MLStripper()
            s.feed(html)
            return s.get_data()
        
        return strip_tags(html)
        