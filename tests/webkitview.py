import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import WebKit
import threading
import time

# Use threads                                       
GLib.threads_init()
Gdk.threads_init()
class App(object):
    def __init__(self): #, app
        #self.application = app
        
        print ('In the app')
        window = Gtk.Window()
        window.connect('key-press-event', self.__key_press_event)
        #window.connect('delete-event',   self.application.on_destroy)
        
        # https://lists.webkit.org/pipermail/webkit-gtk/2011-November/000813.html
        print ('In webkit')
        Gdk.threads_leave()
        Gdk.threads_enter()    
        webView = WebKit.WebView()
        import random
        webView.load_uri('http://google.com/' + str(random.random()))
        Gdk.threads_leave()
        
        window.add(webView)
        window.show_all()
        
        webView.load_uri('http://www.google.com') # Here it works on main thread
        
        self.window = window
        self.webView = webView

    def show_html(self):
        print ('show html')
                    
        time.sleep(1)
        print ('after sleep')
        
        # Update widget in main thread             
        GLib.idle_add(self.webView.load_uri, 'http://www.google.com') # Here it doesn't work

    def __key_press_event(self, widget, event) :
        # event.keyval == Gdk.keyval_from_name("w")

        if event.string == 'q' :
            print (widget)
            self.window.destroy()
            self.webView.destroy()
            #self.application.on_destroy(widget, event) 
            widget.destroy()
            import sys
            sys.exit(0)
            
        elif event.string == 'f' :
            self.unfullscreen()
app = App()

#thread = threading.Thread(target=app.show_html)
#thread.start()

#app.run()
Gtk.main()