from gi.repository import Gtk

class MyLayout(Gtk.Layout):
    def __init__(self, document, **args):
        Gtk.Layout.__init__(self, **args)
        doc_width = 0
        doc_height = 0
        self.document = document

        # Determine the size of the document, I want to display
        for page in self.document.pages:
            doc_width = max(doc_width, page.width)
            doc_height += page.height
        self.aspect_ratio = doc_height / doc_width

        self.connect("draw", self.draw)
    
    def do_realize(self):
        Gtk.Layout.do_realize(self)
        print ('do_realize')

    def do_show(self):
        Gtk.Layout.do_show(self)
        print ('do_show')
        
    def do_draw(self, widget):
        Gtk.Layout.do_draw(self, widget)
        print ('do_draw'), widget

    def draw(self, widget, context):
        print widget, context
        w = self.get_allocated_width()
        h = self.get_allocated_width() * self.aspect_ratio
        self.set_size(w, h) # sets the _content_ size, not the actual widget size
        print("draw")

class page(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
class document(object):
    def __init__(self):
        self.pages = [page(20, 10), page(40, 30)]

layout = MyLayout(document())
win = Gtk.Window()
layout.show()
win.add(layout)
win.show()
Gtk.main()