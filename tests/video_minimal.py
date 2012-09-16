from gi.repository import GdkX11, Gtk

class App:
    def __init__(self):
        win = Gtk.Window()
        win.resize(400, 400)
        win.set_resizable(False)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_double_buffered(True)
        
        hbox = Gtk.HBox()
        win.set_size_request(840, 480)
        
        #win.connect('destroy', self.on_destroy)
        #win.connect('delete-event', self.on_delete_event)

        da = Gtk.DrawingArea()
        
        button = Gtk.Button('Hello')
        button.show()
        
        hbox.pack_start(da, True, True, True)
        hbox.pack_start(button, True, True, True)
        win.add(hbox)
        
        win.show_all()

        print da.get_property('window').get_xid()

if __name__ == "__main__":
    App()
    Gtk.main()