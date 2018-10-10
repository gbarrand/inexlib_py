# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

import inlib

h = inlib.histo_h1d('Rand gauss',100,-5,5)

r = inlib.rgaussd(0,1)
for I in range(0,10000):
  h.fill(r.shoot(),1)

print(h.entries());print(h.mean());print(h.rms())

del r
del h

                
