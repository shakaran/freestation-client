from gi.repository import Gtk, GObject, WebKit

web_view = WebKit.WebView()
web_view.load_uri('http://www.google.com')
 
window = Gtk.Window()
window.add(web_view)
window.show_all()

Gtk.main()