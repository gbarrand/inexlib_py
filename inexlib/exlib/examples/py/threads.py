# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import time
from threading import Thread

def myfunc(i):
    print "sleeping 5 sec from thread %d" % i
    time.sleep(5)
    print "finished sleeping from thread %d" % i

for i in range(3):
    t = Thread(target=myfunc, args=(i,))
    t.start()
