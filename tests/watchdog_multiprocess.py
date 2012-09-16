import time, multiprocessing
from freestationapp2 import FreeStationApp2

from gi.repository import Gtk, Gdk, GObject #@UnresolvedImport

GObject.threads_init()
Gdk.threads_init()
        
def abc():
    p = FreeStationApp2()
    p.run()

p = multiprocessing.Process(target=abc)
p.start()
while(1):
    time.sleep(1)
    if(p.is_alive()==False):
        print ("restarting process")
        p = multiprocessing.Process(target=abc)
        p.start()
    else:
        print ("process still running")