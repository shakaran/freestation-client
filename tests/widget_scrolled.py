#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gdk, Gtk
from gi.repository import GObject #@UnresolvedImport

class ScrolledBox(Gtk.Box):
    __gsignals__ = { 'set-scroll-adjustments' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (Gtk.Adjustment, Gtk.Adjustment)) }
 
    def __init__(self):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 0)
        #self.set_set_scroll_adjustments_signal("set-scroll-adjustments")
        
        #adj = Gtk.Adjustment(0.8, 0.0, 1.0, 0.1, 0.1, 0.1)
        #self.set_scroll_adjustments(adj, adj)
        
window = Gtk.Window()

items_box = ScrolledBox()
items_box.pack_start(Gtk.Button('Button 1 Bla Bla Bla'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 2'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 3 Bla Bla Bla Bla Bla Bla'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 4'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 5 Bla Bla Bla Bla Bla Bla Bla Bla Bla Bla Bla Bla'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 6'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 7'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 8'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 9'), expand = True, fill = True, padding = 0)
items_box.pack_start(Gtk.Button('Button 10'), expand = True, fill = True, padding = 0)

view = Gtk.ScrolledWindow()
            
view.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        

view.add_with_viewport(items_box) 

hbox = Gtk.HBox()
hbox.pack_start(Gtk.Label('The right buttons should be scrolled'), expand = True, fill = True, padding = 0)
hbox.pack_start(view, expand = True, fill = True, padding = 0)

window.add(hbox)
window.show_all()

Gtk.main()