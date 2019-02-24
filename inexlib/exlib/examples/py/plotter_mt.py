# Copyright (C) 2010, Guy Barrand. All rights reserved.
# See the file exlib.license for terms.

# Attempting to have the viewer in another process by using the threading module.
# Should be started with :
#   Python> import plotter_mt
# To stop :
#   Python> plotter_mt.stop_thread = True

# X11/Linux : ok.
# Cocoa, Windows : it does not work.

#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////
import inlib

#//////////////////////////////////////////////////////////
#/// create and fill histogram : //////////////////////////
#//////////////////////////////////////////////////////////
h = inlib.histo_h1d('Rand gauss',100,-5,5)

r = inlib.rgaussd(0,1)
for I in range(0,10000): h.fill(r.shoot(),1)
del r

#print h.entries(),h.mean(),h.rms()

#//////////////////////////////////////////////////////////
#/// plotting : ///////////////////////////////////////////
#//////////////////////////////////////////////////////////
import exlib_window as exlib

stop_thread = False

def plot_histo(a_h,a_stop):
  
  import window
  p = window.plotter(inlib.get_cout(),1,1,0,0,700,500)
  p.plot_histo_cp(a_h)
  p.show()
  
  print('steer...')
  #p.steer() # it blocks input from the prompt (because threading module is not a truely thread system).
  
  import time
  while True:
    if a_stop() == True : break
    if p.sync() == False : break
    time.sleep(0.01)

  print('end steer.')
  del p

  import offscreen
  p = offscreen.plotter(inlib.get_cout(),0,0,700,500)
  p.plot_histo_cp(a_h)
  p.out_ps()
  p.out_zb_ps()
  p.out_bsg()
  del p
  
import threading

_thread = threading.Thread(target=plot_histo, args=(h,lambda: stop_thread))

print('stop viewer thread by closing the window or with : plotter_mt.stop_thread = True')

_thread.start()

del h


                
